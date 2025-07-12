# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# REMOVED: from backend import crud, schemas (redundant)
from backend.database import get_db, User, PasswordResetToken # <--- Corrected to get_db
from dotenv import load_dotenv
from .. import crud, schemas # This import is sufficient
import os

load_dotenv()

# 環境変数から設定を読み込み
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) #環境変数は常に文字列で返されるのでintで数値に直す必要がある
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set.")
if not GOOGLE_CLIENT_ID:
    print("Warning: GOOGLE_CLIENT_ID not set. Google Auth will not work.")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # 認証が必要なエンドポイントで利用
#OAuth2PasswordBearerの役割：リクエストヘッダーから自動でbearerトークンを抽出
#tokenUrlはSwaggerUIの各エンドポイントの検証の手間を省くために渡してる

#APIRouterでルーターのインスタンスを作成
router = APIRouter(prefix="/auth", tags=["auth"]) #prefixに指定したものがこのファイルのすべてのエンドポイントのパスの前につく/tags：SwaggerUIでの各エンドポイントのグループ分け


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

# ④ ユーザー新規登録
@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)): # <--- CHANGED HERE
    db_user = crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = crud.create_user(db=db, user=user_in, auth_provider="local")

    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
    )
    # NOTE: schemas.Token has only 'access_token' and 'token_type'.
    # Returning user_id, email, name, auth_provider here will cause Pydantic validation issues
    # unless you update schemas.Token or use a different response_model.
    # For now, I'm keeping your original return structure, but be aware of this.
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id, # This field is likely not defined in schemas.Token
        email=user.email, # This field is likely not defined in schemas.Token
        name=user.name, # This field is likely not defined in schemas.Token
        auth_provider=user.auth_provider # This field is likely not defined in schemas.Token
    )

# ⑤ ユーザーログイン (ローカル認証)
@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): # <--- CHANGED HERE
    user = crud.get_user_by_email(db, email=form_data.username) # OAuth2PasswordRequestFormはusernameフィールドを使用
    if not user or user.auth_provider != "local" or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password, or account uses Google authentication.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
    )
    # NOTE: Same Pydantic validation warning as above for schemas.Token.
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        name=user.name,
        auth_provider=user.auth_provider
    )

# Google認証
@router.post("/google", response_model=schemas.Token)
async def google_auth(id_token_str: str, db: Session = Depends(get_db)): # <--- CHANGED HERE
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
            user_create_data = schemas.UserCreate(email=email, password=None, name=name) # passwordはダミーとして渡す
            user = crud.create_user(db=db, user=user_create_data, auth_provider='google', google_sub=google_sub)

        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider, "name": user.name}
        )
        # NOTE: Same Pydantic validation warning as above for schemas.Token.
        return schemas.Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            name=user.name,
            auth_provider=user.auth_provider
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google ID token: {e}"
        )
    except Exception as e:
        # ロギングを強化する
        print(f"Google auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during Google authentication."
        )

# ⑥ パスワード再設定要求
@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)): # <--- CHANGED HERE
    user = crud.get_user_by_email(db, email=request.email)
    if user and user.auth_provider == "local": # ローカル認証ユーザーのみ再設定可能
        # トークンを生成してDBに保存
        reset_token = crud.create_password_reset_token(db, user_id=user.id)
        
        # --- ここでメール送信ロジックを実装 ---
        # 例: send_email(user.email, "パスワード再設定", f"http://your-frontend.com/reset-password?token={reset_token.token}")
        print(f"Password reset link for {user.email}: http://your-frontend.com/reset-password?token={reset_token.token}")
        # ------------------------------------

    # セキュリティのため、ユーザーが存在しない場合でも同じ成功メッセージを返す
    return {"message": "If an account with that email exists, a password reset link has been sent."}

# ⑦ パスワード再設定実行
@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)): # <--- CHANGED HERE
    reset_token_db = crud.get_password_reset_token(db, token=request.token)

    if not reset_token_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token.")

    user = crud.get_user_by_id(db, user_id=reset_token_db.user_id)
    if not user or user.auth_provider != "local":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.") # 不正なユーザー、または認証方式が異なる

    # パスワードを更新
    user.hashed_password = crud.get_password_hash(request.new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # 使用済みトークンを削除
    crud.invalidate_password_reset_token(db, reset_token_db)

    return {"message": "Password has been reset successfully."}

# ⑧ ユーザープロフィール取得
@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user