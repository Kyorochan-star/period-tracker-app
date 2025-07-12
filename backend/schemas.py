#schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum
from typing import List, Literal

# ==== Enum for Chat Mode ====
#Enum:決められた選択肢のみを許可する仕組み
class ChatMode(str, Enum):
    PRINCE = "PRINCE"
    MOM = "MOM"
    GRANDMA = "GRANDMA"
    BOYFRIEND = "BOYFRIEND"
    NURSE = "NURSE"

# ==== User関連スキーマ ====
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None

class UserCreate(UserBase):
    # ローカル認証の場合は必須、Google認証の場合はNone。
    # APIロジック側でauth_providerに応じて必須チェックを行う。
    password: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    auth_provider: str # 'local' or 'google'
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

# 認証トークンレスポンス
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenResponse(Token):
    user_id: int
    email: str
    name: Optional[str] = None
    auth_provider: str
    class Config:
        orm_mode = True

# パスワードリセット関連
class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# ==== Period関連スキーマ ====
class PeriodBase(BaseModel):
    start_date: date
    # end_dateは通常、後から更新されるため、ここではオプションにしておく
    end_date: Optional[date] = None # <-- ここを修正: Optional[date] = None が正しい

class PeriodCreateResponse(BaseModel):
    id: int
    user_id: int
    start_date: date
    prediction_end_date: Optional[date] = None # この生理の予測終了日として
    created_at: datetime

class PeriodFullResponse(BaseModel):
    id: int
    user_id: int
    start_date: date
    end_date: Optional[date] = None # 更新時に設定される可能性
    prediction_next_start_date: Optional[date] = None # 更新時に計算される可能性
    prediction_end_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime # 更新時に設定される
class PeriodCreate(PeriodBase):
    # 新規作成時にend_dateも提供される可能性があるため、Baseを継承しつつ、
    # 必要に応じてend_dateにNone以外の値も許可する
    pass

class PeriodUpdate(BaseModel): # <-- ここを修正: PeriodBaseではなくBaseModelから継承し、全てのフィールドをOptionalに
    # 部分更新のため、全てのフィールドをOptionalに
    start_date: Optional[date] = None
    end_date: Optional[date] = None # <-- ここを修正: Optional[date] = None が正しい

class PeriodResponse(PeriodBase):
    id: int
    user_id: int
    prediction_next_start_date: Optional[date] = None
    prediction_end_date: Optional[date] = None
    created_at: datetime
    #updated_at: datetime
    class Config:
        orm_mode = True

# ==== ChatMessage関連スキーマ ====

#スキーマ：データの形式を定義するルール（入力データの検証、出力データの整形）
class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatMessageCreate(BaseModel):
    mode: str  # "boyfriend", "prince", "nurse", "grandma", "mother"
    messages: List[Message]

class ChatMessageResponse(BaseModel):
    id: int
    user_id: int
    mode: str
    query: str
    ai_response: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    mode: ChatMode
    messages: List[Message]


