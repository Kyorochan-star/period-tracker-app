from sqlalchemy.orm import Session
from .database import User, Period, PasswordResetToken, ChatMessage
from .schemas import UserCreate, PeriodCreate, PeriodUpdate, UserUpdate, ChatMessageCreate
from datetime import date, timedelta, datetime, timezone
from passlib.context import CryptContext
import uuid
from typing import List, Optional

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

def calculate_average_period_data(db: Session, user_id: int) -> tuple[int, int]:
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

    avg_period_length = int(sum(period_lengths) / len(period_lengths)) if period_lengths else 5
    avg_cycle_length = int(sum(cycle_lengths) / len(cycle_lengths)) if cycle_lengths else 28

    return avg_period_length, avg_cycle_length

def create_period(db: Session, period: PeriodCreate, user_id: int) -> Period:
    """
    新しい生理期間記録を作成します。
    """
    # crud.py 内で prediction のロジックを実行
    avg_period_length, avg_cycle_length = calculate_average_period_data(db, user_id)

    # 次回生理の予測開始日 (今回のstart_date + 平均周期)
    # create_period の引数 period: PeriodCreate には end_date がある可能性があるので考慮
    # しかし、コメントによると「開始日のみが提供され、終了日は後で更新されます。」とあるので
    # initial end_date は None が想定されている。
    # もし PeriodCreate に end_date が含まれることがあるなら、その値を初期値として使う。
    initial_end_date = period.end_date if period.end_date else None # period.end_date があればそれを使う

    # prediction_next_start_date は、現在のstart_dateを基準に計算される
    prediction_next_start_date = period.start_date + timedelta(days=avg_cycle_length)
    prediction_next_end_date = prediction_next_start_date + timedelta(days=avg_period_length - 1)

    db_period = Period(
        user_id=user_id,
        start_date=period.start_date,
        end_date=initial_end_date, # 初期値を設定
        prediction_next_start_date=prediction_next_start_date,
        prediction_next_end_date=prediction_next_end_date,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period


def get_periods(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None, # <-- 追加
    end_date: Optional[date] = None   # <-- 追加
) -> List[Period]:
    """
    指定されたユーザーの生理記録を全て取得します（フィルタリングオプション付き）。
    """
    query = db.query(Period).filter(Period.user_id == user_id)
    if start_date:
        query = query.filter(Period.start_date >= start_date)
    if end_date:
        # end_dateが指定された場合、その日付以前に終了する期間を対象にする
        # または、開始日がend_date以前の期間も対象にするなど、要件に応じて調整
        query = query.filter(Period.start_date <= end_date) # 簡易的なフィルタリング
        # 例: Period.end_date <= end_date.
        # カレンダー表示の意図を汲むと、指定された期間内に開始する期間を取得するのが一般的です。

    return query.order_by(Period.start_date.desc()).offset(skip).limit(limit).all() # 最新から表示


def get_period_by_id(db: Session, period_id: int, user_id: int) -> Optional[Period]: # user_idを追加
    """
    指定されたIDの生理記録を取得します（ユーザーIDでフィルタリング）。
    """
    return db.query(Period).filter(Period.id == period_id, Period.user_id == user_id).first()

def update_period(db: Session, db_period: Period, period_update: PeriodUpdate) -> Period:
    """
    生理期間記録を更新します。
    end_dateが設定または変更された場合、次回の予測日を再計算します。
    """
    # Pydanticのmodel_dumpでNoneのフィールドも含むように変更 (exclude_none=False)
    # ただし、unsetのフィールドは除外 (exclude_unset=True)
    update_data = period_update.model_dump(exclude_unset=True, exclude_none=False)

    # end_dateが更新されたか、またはNoneに設定されたかをチェック
    if "end_date" in update_data: # キーが存在すれば、Noneであっても更新対象
        db_period.end_date = update_data["end_date"]
    
    # end_dateが設定または変更された場合、またはstart_dateが変更された場合に予測を再計算
    # 予測はstart_dateと過去のデータに依存するため、start_date変更時も再計算が必要
    recalculate_prediction = False
    if "start_date" in update_data and update_data["start_date"] != db_period.start_date:
        db_period.start_date = update_data["start_date"]
        recalculate_prediction = True
    
    # end_dateの変更（Noneから値へ、または値から別の値へ、または値からNoneへ）
    # `is_end_date_modified` を判定するためのロジック
    # `update_data` に `end_date` が含まれていれば、ユーザーが明示的に値を設定（またはNoneに）しようとしている
    # したがって、その値を使って `db_period.end_date` を更新し、予測再計算のトリガーとする
    if "end_date" in update_data:
        # db_period.end_date = update_data["end_date"] # すでに上の `if "end_date" in update_data:` で設定済み
        recalculate_prediction = True # end_dateが変更されたら予測を再計算

    if recalculate_prediction:
        avg_period_length, avg_cycle_length = calculate_average_period_data(db, db_period.user_id)
        
        # prediction_next_start_date は常に現在のperiod.start_dateを基準に計算
        # 今回の生理の開始日が確定しているので、それを基準にする
        prediction_next_start_date = db_period.start_date + timedelta(days=avg_cycle_length)
        #prediction_next_end_date = prediction_next_start_date + timedelta(days=avg_period_length - 1)

        db_period.prediction_next_start_date = prediction_next_start_date
        #db_period.prediction_next_end_date = prediction_next_end_date
    
    # その他のフィールドの更新 (予測関連とcreated_atは直接設定または更新しない)
    for key, value in update_data.items():
        if key not in ["id", "user_id", "prediction_next_start_date", "prediction_next_end_date", "created_at", "start_date", "end_date"]:
            setattr(db_period, key, value)
            
    db_period.updated_at = datetime.now(timezone.utc)
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period

def delete_period(db: Session, period_id: int, user_id: int) -> bool: # user_idを追加
    """
    指定されたIDの生理記録を削除します（ユーザーIDでフィルタリング）。
    """
    db_period = db.query(Period).filter(Period.id == period_id, Period.user_id == user_id).first()
    if db_period:
        db.delete(db_period)
        db.commit()
        return True
    return False

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