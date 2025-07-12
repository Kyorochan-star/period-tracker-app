# backend/database.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey, func, event, JSON
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from typing import Generator
from datetime import datetime, timezone # timezone をインポート


# 環境変数の読み込み
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLiteの場合、check_same_thread=Falseが必要
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ==== ORM Models ====
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True) # Google認証の場合はNULL
    auth_provider = Column(String, default="local", nullable=False) # 'local' or 'google'
    google_sub = Column(String, unique=True, index=True, nullable=True) # Googleの一意なID
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    periods = relationship("Period", back_populates="owner")
    chat_messages = relationship("ChatMessage", back_populates="owner") # ChatMessageとのリレーションを追加
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user") # PasswordResetTokenとのリレーションを追加


class Period(Base):
    __tablename__ = "periods"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True) # 生理進行中はNULL
    # 次回生理の開始予測日
    prediction_next_start_date = Column(Date, nullable=True)
    # 次回生理の終了予測日 (フィールド名を変更)
    prediction_end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    owner = relationship("User", back_populates="periods")

# ==== Database Utility Functions ====
def init_db_connection():
    """データベーステーブルを全て作成します。"""
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized.")

# get_db_session を get_db に変更
def get_db() -> Generator: # <--- ここを変更しました
    """FastAPIの依存性注入でデータベースセッションを提供するジェネレーター。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==== 新しく追加するチャットメッセージモデル ====

class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mode = Column(String, nullable=False)
    messages = Column(JSON, nullable=False)  # messages配列をそのままJSONで保存
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(String, nullable=False) # ユーザーからの質問
    response = Column(String, nullable=False) # AIからの回答
    # timestampのデフォルト値を変更: func.now() を使用し、データベースのタイムスタンプを反映
    timestamp = Column(DateTime, default=func.now())

    owner = relationship("User", back_populates="chat_messages") # リレーションシップ名を修正


# パスワードリセットトークン管理用のテーブル (オプション、必要に応じて追加)
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="password_reset_tokens") # リレーションシップ名を修正