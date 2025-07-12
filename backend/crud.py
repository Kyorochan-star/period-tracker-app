from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, asc # SQLAlchemyの関数もインポート
from .database import User, Period, PasswordResetToken, ChatMessage
from .schemas import UserCreate, PeriodCreate, PeriodUpdate, UserUpdate, ChatMessageCreate
from datetime import date, timedelta, datetime, timezone
from passlib.context import CryptContext
import uuid
from typing import List, Optional,Tuple

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ==== User CRUD ====

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

# この関数はschemas.UserCreateがusernameを含まないため、通常は不要です。
# もし必要ならUserモデルにusernameフィールドがあることを確認してください。
# def get_user_by_username(db: Session, username: str) -> Optional[User]:
#    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate, auth_provider: str = "local") -> User:
    """
    新しいユーザーを作成します。
    """
    hashed_password = None
    if user.password: # パスワードが提供されている場合のみハッシュ化
        hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        hashed_password=hashed_password, # Noneの場合もそのままセット
        name=user.name,
        auth_provider=auth_provider,
        created_at=datetime.now(timezone.utc), # 追加
        updated_at=datetime.now(timezone.utc)  # 追加
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ==== Period CRUD ====

# get_user_by_id は get_user と同じ機能なので、どちらか一方に統一することを検討
# 今回は get_user で統一するため、この関数はコメントアウトまたは削除します。
# def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
#     return db.query(User).filter(User.id == user_id).first()

def calculate_average_period_data(db: Session, user_id: int) -> Tuple[int, int]:
    """
    ユーザーの過去の生理記録から、平均生理期間と平均生理周期を計算します。
    """
    past_periods = db.query(Period).filter(
        Period.user_id == user_id,
        Period.start_date.isnot(None),
        Period.end_date.isnot(None)
    ).order_by(Period.start_date.asc()).all()

    period_lengths = []
    cycle_lengths = []

    for i, current_period in enumerate(past_periods):
        if current_period.end_date and current_period.start_date:
            period_length = (current_period.end_date - current_period.start_date).days + 1
            period_lengths.append(period_length)

        if i + 1 < len(past_periods):
            next_period = past_periods[i+1]
            if next_period.start_date and current_period.start_date:
                cycle_length = (next_period.start_date - current_period.start_date).days
                cycle_lengths.append(cycle_length)

    # 計算ロジックを修正 (四捨五入して+1を削除)
    avg_period_length = int(round(sum(period_lengths) / len(period_lengths))) if period_lengths else 5
    avg_cycle_length = int(round(sum(cycle_lengths) / len(cycle_lengths))) if cycle_lengths else 28

    return avg_period_length, avg_cycle_length


def create_period(db: Session, period: PeriodCreate, user_id: int) -> Period:
    """
    新しい生理期間記録を作成します。
    この関数は、「この生理の予測終了日」を計算し、`prediction_end_date`に保存します。
    """
    avg_period_length, _ = calculate_average_period_data(db, user_id)

    # 「この生理の予測終了日」を計算
    # (start_date + 平均生理期間日数 - 1日)
    predicted_current_period_end_date = period.start_date + timedelta(days=avg_period_length - 1)

    db_period = Period(
        user_id=user_id,
        start_date=period.start_date,
        # *** ここを変更 ***
        # 「この生理の予測終了日」を prediction_end_date カラムに保存する
        prediction_end_date=predicted_current_period_end_date,
        # prediction_next_start_date はここでは設定しない（通常はend_date記録後に計算）
        prediction_next_start_date=None, # 明示的にNone
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(db_period)
    db.commit()
    db.refresh(db_period) # DBが生成したIDなどを取得するためにリフレッシュ
    return db_period



def get_periods(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100, # こちらのlimitを残し、重複している方を削除します
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    order_by: str = "start_date", # 追加された引数
    order_direction: str = "desc", # 追加された引数
) -> List[Period]:
    """
    指定されたユーザーの生理記録を全て取得します（フィルタリングオプション付き）。
    """
    query = db.query(Period).filter(Period.user_id == user_id)

def get_periods(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100, # 重複を解消し、デフォルト値を設定
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    order_by: str = "start_date",
    order_direction: str = "desc",
) -> List[Period]:
    """
    指定されたユーザーの生理記録を全て取得します（フィルタリングオプション付き）。
    """
    query = db.query(Period).filter(Period.user_id == user_id)

    # --- 全てのフィルタリングロジックをここにまとめる ---
    # Period が database.py から直接インポートされているため、Period を直接使う
    if start_date and end_date:
        # 開始日が指定期間の終了日以前、かつ
        # (終了日が指定期間の開始日以降、または終了日がNULL)
        query = query.filter(
            and_(
                Period.start_date <= end_date,
                (Period.end_date >= start_date) | (Period.end_date.is_(None)) # .is_(None) を使用
            )
        )
    elif start_date: # start_dateのみ指定の場合
        query = query.filter(Period.start_date >= start_date)
    elif end_date: # end_dateのみ指定の場合
        # 指定されたend_dateまでに開始する生理期間
        query = query.filter(Period.start_date <= end_date)

    # --- ソートの適用 (フィルタリングの後) ---
    if order_direction == "desc":
        query = query.order_by(desc(getattr(Period, order_by)))
    else:
        query = query.order_by(asc(getattr(Period, order_by)))

    # --- オフセットとリミットの適用 (ソートの後) ---
    # これらを一度だけ、正しく適用します
    query = query.offset(skip).limit(limit)

    # --- クエリの実行 ---
    # 最終的なクエリを .all() で実行します。
    # ここで order_by, offset, limit を再度呼び出さない
    return query.all()

def get_period_by_id(db: Session, period_id: int, user_id: int) -> Optional[Period]:
    """
    指定されたIDの生理記録を取得します（ユーザーIDでフィルタリング）。
    """
    return db.query(Period).filter(Period.id == period_id, Period.user_id == user_id).first()


def update_period(db: Session, db_period: Period, period_update: PeriodUpdate) -> Period:
    """
    生理期間記録を更新します。
    start_dateまたはend_dateが変更された場合、関連する予測日を再計算します。
    """
    # 変更前のstart_dateとend_dateを保持 (変更があったか確認するため)
    original_start_date = db_period.start_date
    original_end_date = db_period.end_date

    # Pydanticモデルから更新データを取得
    # exclude_unset=True: リクエストに含まれないフィールドは更新しない
    # exclude_none=False: Noneが指定された場合は、そのフィールドをNoneで更新する
    update_data = period_update.model_dump(exclude_unset=True, exclude_none=False)

    # まず、受け取った更新データをdb_periodオブジェクトに一括で適用する
    # id, user_id, created_at, updated_at, prediction_next_start_date, prediction_end_date
    # といったフィールドはユーザーから直接更新されない、または自動計算されるため除外リストに入れる
    # start_date, end_date は予測計算のトリガーなので、後で個別にチェック
    fields_to_exclude_from_direct_update = [
        "id", "user_id", "created_at", "updated_at",
        "prediction_next_start_date", "prediction_end_date",
        "start_date", "end_date" # start_dateとend_dateは後で個別に処理するため、ここでは除外
    ]

    for key, value in update_data.items():
        if key not in fields_to_exclude_from_direct_update:
            setattr(db_period, key, value)

    # start_date と end_date の更新は個別に行い、変更フラグを立てる
    is_start_date_changed = False
    is_end_date_changed = False

    if "start_date" in update_data:
        if db_period.start_date != update_data["start_date"]: # 実際に値が変わったか
            is_start_date_changed = True
        db_period.start_date = update_data["start_date"] # 新しい値をセット

    if "end_date" in update_data:
        # 現在の値と新しい値（Noneも含む）が異なる場合に変更フラグを立てる
        if db_period.end_date != update_data["end_date"]:
            is_end_date_changed = True
        db_period.end_date = update_data["end_date"] # 新しい値をセット

    # 予測の再計算が必要かどうかの判断
    # start_date または end_date のいずれかが変更された場合に予測を再計算する
    if is_start_date_changed or is_end_date_changed:
        avg_period_length, avg_cycle_length = calculate_average_period_data(db, db_period.user_id)
        
        # prediction_end_date (この生理の予測終了日) は start_date を基準に常に再計算
        db_period.prediction_end_date = db_period.start_date + timedelta(days=avg_period_length - 1)

        # prediction_next_start_date (次回の生理予測開始日) は end_date が確定した場合に計算
        if db_period.end_date is not None:
            # 一般的に、次回の生理開始日は今回の生理開始日 + 平均生理周期 で計算されることが多い
            # もし「今回の生理終了日 + 平均周期」であればロジックを変更
            db_period.prediction_next_start_date = db_period.start_date + timedelta(days=avg_cycle_length)
        else:
            # end_dateがNoneの場合は次回の予測日もNoneにする
            db_period.prediction_next_start_date = None

    # updated_at は常に更新
    db_period.updated_at = datetime.now(timezone.utc)
    
    db.add(db_period) # 変更をステージング
    db.commit() # データベースに保存
    db.refresh(db_period) # 最新の状態をリフレッシュ
    return db_period

# def delete_period(db: Session, period_id: int, user_id: int) -> bool: # user_idを追加
#     """
#     指定されたIDの生理記録を削除します（ユーザーIDでフィルタリング）。
#     """
#     db_period = db.query(Period).filter(Period.id == period_id, Period.user_id == user_id).first()
#     if db_period:
#         db.delete(db_period)
#         db.commit()
#         return True
#     return False

# ==== Password Reset Token CRUD ====

def create_password_reset_token(db: Session, user_id: int) -> PasswordResetToken:
    token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    db_token = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_password_reset_token(db: Session, token: str) -> Optional[PasswordResetToken]:
    return db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.expires_at > datetime.now(timezone.utc)
    ).first()

def delete_password_reset_token(db: Session, token_id: int) -> bool:
    db_token = db.query(PasswordResetToken).filter(PasswordResetToken.id == token_id).first()
    if db_token:
        db.delete(db_token)
        db.commit()
        return True
    return False

# ==== ChatMessage CRUD ====

def create_chat_message(db: Session, chat_message: ChatMessageCreate, user_id: int, ai_response: str) -> ChatMessage:
    db_chat_message = ChatMessage(
        user_id=user_id,
        query=chat_message.query,
        response=ai_response,
        timestamp=datetime.now(timezone.utc),
        mode=chat_message.mode # <-- chat_message.mode も保存する
    )
    db.add(db_chat_message)
    db.commit()
    db.refresh(db_chat_message) #db_chat_messageオブジェクト(インスタンス)を最新状態に更新
    return db_chat_message 

def get_chat_messages(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[ChatMessage]:
    return db.query(ChatMessage).filter(ChatMessage.user_id == user_id).order_by(ChatMessage.timestamp.desc()).offset(skip).limit(limit).all()