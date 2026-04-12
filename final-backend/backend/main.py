import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
# docker-composeを使わないローカル実行時のために読み込む
from dotenv import load_dotenv
#CORS
from fastapi.middleware.cors import CORSMiddleware
from connect import get_connection


# .envファイルから環境変数をロード
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAIクライアントの初期化
# APIキーは環境変数から自動的に読み込まれますが、明示的に渡すことも可能です
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

#保存用の関数
def save_message(conversation_id: str, role: str, content: str, model: str):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO messages (conversation_id, role, content, model)
            VALUES (%s, %s, %s, %s)
            """,
            (conversation_id, role, content, model)
        )
        conn.commit()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#履歴の取得
@app.get("/messages/{conversation_id}")
def get_messages(conversation_id : str) :
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT role, content, model, created_at
            FROM (
                SELECT role, content
                FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            ) sub
            WHERE conversation_id = %s
            ORDER BY created_at ASC
            """,
            (conversation_id,)
        )

        rows = cur.fetchall()

        messages = []
        for row in rows:
            messages.append({
                "role": row[0],
                "content": row[1],
                "model": row[2],
                "created_at": str(row[3])
            })

        return {"messages": messages}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#過去履歴
def get_conversation_history(conversation_id: str, limit: int = 10):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT role, content
            FROM messages
            WHERE conversation_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (conversation_id, limit)
        )

        rows = cur.fetchall()

        history = []
        for row in rows:
            history.append({
                "role": "assistant" if row[0] == "ai" else row[0],
                "content": row[1]
            })

        return history

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# リクエストボディの定義（ユーザーから送られてくるデータの型）
class ChatRequest(BaseModel):
    message: str
    conversation_id: str

@app.post("/chat")
def chat(request: ChatRequest):
    """
    ユーザーからのメッセージを受け取り、AIの返答を返すエンドポイント
    """
    try:
        model_name = "gpt-4o-mini"

        # ユーザーからの発言の保存
        save_message(
            request.conversation_id,
            "user",
            request.message,
            model_name
        )

        history = get_conversation_history(request.conversation_id, 10)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=
                [{"role": "system", "content": "あなたは内閣総理大臣の高市早苗です。与えられた質問に対して内閣総理大臣・高市早苗として丁寧に返答することが主な役割です。"}]
                + history +
                [{"role": "user", "content": request.message}]
        )


        print("OpenAI response:", response)
        
        # AIからの返答内容を取得
        ai_message = response.choices[0].message.content

        print("ai_message:", ai_message)

        if ai_message is None:
            ai_message = "回答を取得できませんでした。"

        # AIからの返答の保存
        save_message(
            request.conversation_id,
            "ai",
            ai_message,
            model_name
        )
        
        return {"reply": ai_message}

    except Exception as e:
        # エラーが発生した場合の処理
        return {"error": str(e)}

