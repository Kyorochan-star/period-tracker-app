# backend/routers/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db, User # database.py から get_db と User をインポート
from ..schemas import ChatMessageCreate, ChatMessageResponse, ChatMode # schema.py からスキーマをインポート (UserResponseは削除)
from .. import crud # crud.py から CRUD 関数をインポート
from .auth import get_current_user # 認証済みユーザーを取得する依存関係
import openai
import os

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    dependencies=[Depends(get_current_user)], # このルーターの全エンドポイントで認証が必要
    responses={404: {"description": "Not found"}},
)

# OpenAI APIキーを環境変数から取得
openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    # APIキーが設定されていない場合は、起動時に警告を出すか、エラーを発生させる
    print("WARNING: OpenAI API key is not set. Chat functionality will not work.")

# --- 各モードに対応するシステムメッセージを定義します ---
SYSTEM_MESSAGES = {
    ChatMode.PRINCE: "あなたはユーザーの月経に関する悩みに答える王子様です。常に優しく、励ましの言葉をかけ、ユーザーを安心させるようなロマンチックなトーンで回答してください。ただし、医学的な正確さも保ち、必要に応じて専門医への相談を促してください。",
    ChatMode.MOM: "あなたはユーザーの月経に関する悩みに答える、愛情深いお母さんです。ユーザーの健康を第一に考え、温かく、時には少し心配しながらも、実践的で具体的なアドバイスを与えてください。診断や治療は行わず、必要に応じて専門医への相談を促してください。",
    ChatMode.GRANDMA: "あなたはユーザーの月経に関する悩みに答える、経験豊かで穏やかなおばあちゃんです。昔ながらの知恵や優しい言葉を交えながら、温かく、安心させるようなトーンで回答してください。ただし、医学的な正確さも保ち、必要に応じて専門医への相談を促してください。",
    ChatMode.BOYFRIEND: "あなたはユーザーの月経に関する悩みに寄り添う、理解力のある彼氏です。共感と優しさを最優先し、ユーザーの気持ちに寄り添いながら、支えとなる言葉をかけてください。医学的なアドバイスは控えめにし、専門医への相談を促す際には、一緒に解決しようとする姿勢を見せてください。",
    ChatMode.NURSE: "あなたはユーザーの月経に関する悩みに答える、プロフェッショナルで丁寧な保健室の先生です。正確な医学情報を提供し、落ち着いた、客観的なトーンで分かりやすく説明してください。診断や治療は行わず、必要に応じて専門医への相談を促してください。"
}

def generate_gpt_response(query: str, mode: ChatMode) -> str: # <-- mode引数にデフォルト値なし
    """
    ChatGPT APIを呼び出して応答を生成します。
    ユーザーが選択したモードに基づいてシステムメッセージを切り替えます。
    """
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI APIキーが設定されていません。")

    # 選択されたモードに対応するシステムメッセージを取得
    # ChatMode Enumを使用しているため、modeはSYSTEM_MESSAGESに必ず存在する有効なキーです。
    system_message = SYSTEM_MESSAGES[mode]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", # またはより適切なモデル（例: gpt-4）
            messages=[
                {"role": "system", "content": system_message}, # <-- ここがモードに応じて変わります
                {"role": "user", "content": query}
            ],
            temperature=0.0 # 創造性の度合いを調整（0.0-1.0、低いほど確定的・事実に基づいた回答になりやすい）
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"OpenAI APIエラー: {e}")
        raise HTTPException(status_code=500, detail=f"AIとの通信エラーが発生しました: {e}")
    except Exception as e:
        print(f"予期せぬエラー: {e}")
        raise HTTPException(status_code=500, detail="AI応答生成中に予期せぬエラーが発生しました。")

@router.post("/", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def chat_with_ai(
    chat_message_create: ChatMessageCreate, # Pydanticスキーマを使用
    current_user: User = Depends(get_current_user), # <--- UserResponseからUserに変更
    db: Session = Depends(get_db)
):
    """
    AIに質問を送信し、回答を取得して履歴に保存します。
    ユーザーが選択したモードに基づいてAIの応答を生成します。
    """
    # chat_message_create.mode を generate_gpt_response に渡す
    ai_response = generate_gpt_response(chat_message_create.query, mode=chat_message_create.mode)
    
    # チャット履歴をデータベースに保存
    db_chat_message = crud.create_chat_message(
        db=db,
        chat_message=chat_message_create,
        user_id=current_user.id,
        ai_response=ai_response # AIの回答を渡す
    )
    return db_chat_message

@router.get("/", response_model=list[ChatMessageResponse])
def get_chat_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user), # <--- UserResponseからUserに変更
    db: Session = Depends(get_db)
):
    """
    認証済みユーザーのチャット履歴を取得します。
    """
    return crud.get_chat_messages(db=db, user_id=current_user.id, skip=skip, limit=limit)