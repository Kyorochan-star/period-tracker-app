from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.get("/")
async def read_root():
    """APIのルートエンドポイント。"""
    return {"message": "Welcome to the Period Tracker API!"}

# ユーザー新規登録
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user_mock():
    # MockDataのパス（必要に応じて絶対パスや環境変数で調整）
    mock_path = "PeriodTracker/MockData/User/register_response.json"
    # ファイルを開いてJSONを読み込む
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    # そのまま返すえ
    return JSONResponse(content=mock_data, status_code=status.HTTP_201_CREATED)

# ユーザーログイン (ローカル認証)
@app.post("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token_mock():
    mock_path = "PeriodTracker/MockData/User/login_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)

# Google認証
@app.post("/google", status_code=status.HTTP_200_OK)
async def google_auth_mock():
    mock_path = "PeriodTracker/MockData/User/login_response.json"  # 必要に応じてgoogle用のmockを作成
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)

# パスワード再設定要求
@app.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password_mock():
    mock_path = "PeriodTracker/MockData/Auth/forgot_password_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)

# パスワード再設定実行
@app.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password_mock():
    mock_path = "PeriodTracker/MockData/Auth/reset_password_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)

# ユーザープロフィール取得
@app.get("/me", status_code=status.HTTP_200_OK)
async def read_users_me_mock():
    mock_path = "PeriodTracker/MockData/User/profile_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)


# ① 生理開始記録
@app.post("/period", status_code=status.HTTP_201_CREATED)
async def create_period_entry_mock():
    mock_path = "PeriodTracker/MockData/Period/start_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_201_CREATED)

# ② 生理終了記録 / 生理期間更新
@app.patch("/period/{period_id}", status_code=status.HTTP_200_OK)
async def update_period_entry_mock(period_id: int):
    mock_path = "PeriodTracker/MockData/Period/end_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)

# ③ カレンダー表示＆六ヶ月分の表示
@app.get("/period", status_code=status.HTTP_200_OK)
async def read_periods_mock():
    mock_path = "PeriodTracker/MockData/Period/calendar_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)

# 特定生理期間の取得
# @app.get("/period/{period_id}", status_code=status.HTTP_200_OK)
# async def read_single_period_mock(period_id: int):
#     mock_path = "Period
#     with open(mock_path, "r", encoding="utf-8") as f:
#         mock_data = json.load(f)
#     # 必要に応じてperiod_idでフィルタリングする処理を追加可能
#     return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)

# 生理期間の削除
@app.delete("/period/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_period_entry_mock(period_id: int):
    # 削除は204 No Contentなのでボディなし
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


@app.post("/chat", status_code=status.HTTP_201_CREATED)
async def create_chat_entry_mock():
    mock_path = "PeriodTracker/MockData/Chat/send_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_201_CREATED)

@app.get("/chat", status_code=status.HTTP_200_OK)
async def read_chat_history_mock():
    mock_path = "PeriodTracker/MockData/Chat/history_response.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)
    return JSONResponse(content=mock_data, status_code=status.HTTP_200_OK)