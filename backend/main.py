# backend/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import init_db_connection
# chatルーターをインポートリストに追加
from .routers import auth, periods, chat
from fastapi.middleware.cors import CORSMiddleware


# lifespanコンテキストマネージャーを定義
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクルイベント（起動時とシャットダウン時）を処理します。
    """
    print("Application startup...")
    # データベース接続の初期化をここで行います
    init_db_connection() # データベーステーブルの作成など
    print("Database connection initialized.")
    yield # アプリケーションがリクエストを受け付ける準備ができたことを示します
    # アプリケーションシャットダウン時のクリーンアップ処理があればここに記述
    print("Application shutdown.")

# FastAPIアプリケーションのインスタンスを作成します。
# lifespan引数に定義したlifespan関数を渡します。
app = FastAPI(
    title="Period Tracker API",
    description="API for managing period tracking data and AI consultation.", # 説明を更新
    version="0.1.0",
    lifespan=lifespan, # ここでlifespanを渡す
)

# CORS (Cross-Origin Resource Sharing) 設定
# # フロントエンドが異なるオリジン（ポートやドメイン）にある場合、これが必要
origins = [
    "http://localhost",
    "http://localhost:3000", # 例: React開発サーバー
    # あなたのフロントエンドのURLを追加
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 全てのHTTPメソッドを許可
    allow_headers=["*"], # 全てのヘッダーを許可
)

# アプリケーションのルートエンドポイント
# このルートは、上記の `app = FastAPI(...)` インスタンスに直接関連付けられます。
@app.get("/")
async def read_root():
    """APIのルートエンドポイント。"""
    return {"message": "Welcome to the Period Tracker API!"}


# ルーターをアプリケーションに含める
app.include_router(auth.router)
app.include_router(periods.router)
app.include_router(chat.router) # 新しく追加するチャットルーター