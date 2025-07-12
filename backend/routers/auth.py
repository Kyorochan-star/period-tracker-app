from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# REMOVED: from backend import crud, schemas (redundant)
from ..database import get_db, User, PasswordResetToken # <--- Corrected to get_db
from dotenv import load_dotenv
from .. import crud, schemas # This import is sufficient
import os

load_dotenv()

# 環境変数から設定を読み込み
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set.")
if not GOOGLE_CLIENT_ID:
    print("Warning: GOOGLE_CLIENT_ID not set. Google Auth will not work.")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # 認証が必要なエンドポイントで利用

router = APIRouter(prefix="/auth", tags=["auth"])


# ヘルパー関数：JWTトークン生成
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 依存性注入：現在のユーザーを取得 (保護されたエンドポイントで利用)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User: # <--- CHANGED HERE
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        auth_provider: str = payload.get("auth_provider")
        if user_id is None or auth_provider is None:
            raise credentials_exception
        user = crud.get_user_by_id(db, user_id=user_id)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


# ==== エンドポイントの実装 ====

@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. メールアドレスの重複チェック
    # 同じメールアドレスのユーザーが既に存在するかデータベースで確認します。
    db_user = crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        # 既に登録済みの場合はHTTP 409 Conflictエラーを返します。
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # 2. 新しいユーザーの作成とデータベースへの保存
    # メールアドレスが重複していなければ、crudモジュールを使って新しいユーザーを作成します。
    # auth_provider="local"は、このユーザーがメールとパスワードで認証することを意味します。
    user = crud.create_user(db=db, user=user_in, auth_provider="local")

    # 3. アクセストークンの生成
    # 新規登録に成功したユーザーのために、今後の認証で使用するJWTアクセストークンを生成します。
    # トークンには、ユーザーID、メール、認証プロバイダー、名前などの情報が埋め込まれます。
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
    )

    # 4. レスポンスの返却
    # クライアントにアクセストークンとトークンタイプ（"bearer"）を返します。
    # 通常、schemas.Tokenはaccess_tokenとtoken_typeのみを持ちます。
    # user_idなどの追加情報は、通常は別のエンドポイント（例: /auth/me）で取得されます。
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",

    )

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. ユーザーの取得と認証情報の検証
    # 提供されたメールアドレスでユーザーを検索し、パスワードが一致するか、
    # および認証プロバイダーが"local"（Google認証などではない）であることを確認します。
    user = crud.get_user_by_email(db, email=form_data.username) # OAuth2PasswordRequestFormはusernameフィールドを使用
    if not user or user.auth_provider != "local" or not crud.verify_password(form_data.password, user.hashed_password):
        # 認証に失敗した場合はHTTP 401 Unauthorizedエラーを返します。
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password, or account uses Google authentication.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. アクセストークンの生成
    # 認証に成功したユーザーのために、今後の認証で使用するJWTアクセストークンを生成します。
    # トークンには、ユーザーID、メール、認証プロバイダー、名前などの情報が埋め込まれます。
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
    )

    # 3. レスポンスの返却
    # クライアントにアクセストークンとトークンタイプ（"bearer"）を返します。
    # ここも新規登録と同様に、schemas.Tokenの定義とレスポンスのフィールドが合致するか確認が必要です。
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
    )

# Google認証
@router.post("/google", response_model=schemas.Token)
async def google_auth(id_token_str: str, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), GOOGLE_CLIENT_ID)
        google_sub = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name')

        user = crud.get_user_by_google_sub(db, google_sub=google_sub)

        if user: # 既存のGoogle認証ユーザー
            if user.auth_provider != 'google':
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Account with this Google ID exists but is not set as Google auth provider. Please contact support."
                )
        else: # 新規Google認証ユーザー
            # 同じメールアドレスでローカル認証済みのアカウントがないかチェック
            existing_local_user = crud.get_user_by_email(db, email=email)
            if existing_local_user and existing_local_user.auth_provider == 'local':
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="An account with this email already exists using local authentication. Please log in with your email and password."
                )

            # 新規ユーザー作成（hashed_passwordはNone）
            user_create_data = schemas.UserCreate(email=email, password=None, name=name)
            user = crud.create_user(db=db, user=user_create_data, auth_provider='google', google_sub=google_sub)

        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
        )
        return schemas.Token(
            access_token=access_token,
            token_type="bearer",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google ID token: {e}"
        )
    except Exception as e:
        print(f"Google auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during Google authentication."
        )

# パスワード再設定要求
@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=request.email)
    if user and user.auth_provider == "local": # ローカル認証ユーザーのみ再設定可能
        # トークンを生成してDBに保存
        reset_token = crud.create_password_reset_token(db, user_id=user.id)
        
        # メール送信ロジックを実装する場合はここに追加
        print(f"Password reset link for {user.email}: http://your-frontend.com/reset-password?token={reset_token.token}")

    # セキュリティのため、ユーザーが存在しない場合でも同じ成功メッセージを返す
    return {"message": "If an account with that email exists, a password reset link has been sent."}

# パスワード再設定実行
@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    reset_token_db = crud.get_password_reset_token(db, token=request.token)

    if not reset_token_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token.")

    user = crud.get_user_by_id(db, user_id=reset_token_db.user_id)
    if not user or user.auth_provider != "local":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    # パスワードを更新
    user.hashed_password = crud.get_password_hash(request.new_password)
    user.updated_at = datetime.now(timezone.utc)
    db.commit()

    # 使用済みトークンを削除
    crud.delete_password_reset_token(db, reset_token_db.id)

    return {"message": "Password has been reset successfully."} in schemas.Token
#         auth_provider=user.auth_provider # This field is likely not defined in schemas.Token
#     )

# # ⑤ ユーザーログイン (ローカル認証)
# @router.post("/login", response_model=schemas.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): # <--- CHANGED HERE
#     user = crud.get_user_by_email(db, email=form_data.username) # OAuth2PasswordRequestFormはusernameフィールドを使用
#     if not user or user.auth_provider != "local" or not crud.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password, or account uses Google authentication.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = create_access_token(
#         data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
#     )
#     # NOTE: Same Pydantic validation warning as above for schemas.Token.
#     return schemas.Token(
#         access_token=access_token,
#         token_type="bearer",
#         user_id=user.id,
#         email=user.email,
#         name=user.name,
#         auth_provider=user.auth_provider
#     )

# # Google認証
# @router.post("/google", response_model=schemas.Token)
# async def google_auth(id_token_str: str, db: Session = Depends(get_db)): # <--- CHANGED HERE
#     try:
#         idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), GOOGLE_CLIENT_ID)
#         google_sub = idinfo['sub']
#         email = idinfo['email']
#         name = idinfo.get('name')

#         user = crud.get_user_by_google_sub(db, google_sub=google_sub)

#         if user: # 既存のGoogle認証ユーザー
#             if user.auth_provider != 'google':
#                 raise HTTPException(
#                     status_code=status.HTTP_409_CONFLICT,
#                     detail="Account with this Google ID exists but is not set as Google auth provider. Please contact support."
#                 )
#         else: # 新規Google認証ユーザー
#             # 同じメールアドレスでローカル認証済みのアカウントがないかチェック
#             existing_local_user = crud.get_user_by_email(db, email=email)
#             if existing_local_user and existing_local_user.auth_provider == 'local':
#                 raise HTTPException(
#                     status_code=status.HTTP_409_CONFLICT,
#                     detail="An account with this email already exists using local authentication. Please log in with your email and password."
#                 )

#             # 新規ユーザー作成（hashed_passwordはNone）
#             user_create_data = schemas.UserCreate(email=email, password=None, name=name) # passwordはダミーとして渡す
#             user = crud.create_user(db=db, user=user_create_data, auth_provider='google', google_sub=google_sub)

#         access_token = create_access_token(
#             data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
#         )
#         # NOTE: Same Pydantic validation warning as above for schemas.Token.
#         return schemas.Token(
#             access_token=access_token,
#             token_type="bearer",
#             user_id=user.id,
#             email=user.email,
#             name=user.name,
#             auth_provider=user.auth_provider
#         )

#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Invalid Google ID token: {e}"
#         )
#     except Exception as e:
#         # ロギングを強化する
#         print(f"Google auth error: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred during Google authentication."
#         )

# # ⑥ パスワード再設定要求
# @router.post("/forgot-password", status_code=status.HTTP_200_OK)
# async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)): # <--- CHANGED HERE
#     user = crud.get_user_by_email(db, email=request.email)
#     if user and user.auth_provider == "local": # ローカル認証ユーザーのみ再設定可能
#         # トークンを生成してDBに保存
#         reset_token = crud.create_password_reset_token(db, user_id=user.id)
        
#         # --- ここでメール送信ロジックを実装 ---
#         # 例: send_email(user.email, "パスワード再設定", f"http://your-frontend.com/reset-password?token={reset_token.token}")
#         print(f"Password reset link for {user.email}: http://your-frontend.com/reset-password?token={reset_token.token}")
#         # ------------------------------------

#     # セキュリティのため、ユーザーが存在しない場合でも同じ成功メッセージを返す
#     return {"message": "If an account with that email exists, a password reset link has been sent."}

# # ⑦ パスワード再設定実行
# @router.post("/reset-password", status_code=status.HTTP_200_OK)
# async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)): # <--- CHANGED HERE
#     reset_token_db = crud.get_password_reset_token(db, token=request.token)

#     if not reset_token_db:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token.")

#     user = crud.get_user_by_id(db, user_id=reset_token_db.user_id)
#     if not user or user.auth_provider != "local":
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.") # 不正なユーザー、または認証方式が異なる

#     # パスワードを更新
#     user.hashed_password = crud.get_password_hash(request.new_password)
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     # 使用済みトークンを削除
#     crud.invalidate_password_reset_token(db, reset_token_db)

#     return {"message": "Password has been reset successfully."}

# # ⑧ ユーザープロフィール取得
# @router.get("/me", response_model=schemas.UserResponse)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user