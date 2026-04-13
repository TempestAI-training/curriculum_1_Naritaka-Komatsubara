import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from connect import get_connection

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client():
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    if not api_key or not api_version or not azure_endpoint:
        raise ValueError("Azure OpenAI environment variables are not set properly")

    return AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
    )


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
            (conversation_id, role, content, model),
        )
        conn.commit()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.get("/debug-ping")
def debug_ping():
    print("===== DEBUG PING HIT =====", flush=True)
    return {"ok": True}


@app.get("/messages/{conversation_id}")
def get_messages(conversation_id: str):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT role, content, model, created_at
            FROM messages
            WHERE conversation_id = %s
            ORDER BY created_at ASC
            """,
            (conversation_id,),
        )

        rows = cur.fetchall()

        messages = []
        for row in rows:
            messages.append(
                {
                    "role": row[0],
                    "content": row[1],
                    "model": row[2],
                    "created_at": str(row[3]),
                }
            )

        return {"messages": messages}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


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
            (conversation_id, limit),
        )

        rows = cur.fetchall()

        history = []
        for row in rows:
            history.append(
                {
                    "role": "assistant" if row[0] == "ai" else row[0],
                    "content": row[1],
                }
            )

        # 古い順にしたいので逆順に戻す
        history.reverse()
        return history

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


class ChatRequest(BaseModel):
    message: str
    conversation_id: str


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        print("===== CHAT START =====", flush=True)
        print(f"AZURE_OPENAI_ENDPOINT={os.getenv('AZURE_OPENAI_ENDPOINT')}", flush=True)
        print(f"AZURE_OPENAI_API_VERSION={os.getenv('AZURE_OPENAI_API_VERSION')}", flush=True)
        print(f"AZURE_OPENAI_DEPLOYMENT={os.getenv('AZURE_OPENAI_DEPLOYMENT')}", flush=True)
        print(
            f"AZURE_OPENAI_API_KEY_EXISTS={bool(os.getenv('AZURE_OPENAI_API_KEY'))}",
            flush=True,
        )
        print(
            f"AZURE_OPENAI_API_KEY_LENGTH={len(os.getenv('AZURE_OPENAI_API_KEY') or '')}",
            flush=True,
        )
        print(f"DB_HOST={os.getenv('DB_HOST')}", flush=True)
        print(f"DB_NAME={os.getenv('DB_NAME')}", flush=True)
        print(f"DB_USER={os.getenv('DB_USER')}", flush=True)

        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        if not deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT is not set")

        client = get_client()

        save_message(
            request.conversation_id,
            "user",
            request.message,
            deployment_name,
        )

        history = get_conversation_history(request.conversation_id, 10)

        response = client.chat.completions.create(
            model=deployment_name,
            messages=
            [
                {
                    "role": "system",
                    "content": "あなたは内閣総理大臣の高市早苗です。与えられた質問に対して内閣総理大臣・高市早苗として丁寧に返答することが主な役割です。",
                }
            ]
            + history
            + [{"role": "user", "content": request.message}],
        )

        ai_message = response.choices[0].message.content
        print(f"ai_message={ai_message}", flush=True)

        if ai_message is None:
            ai_message = "回答を取得できませんでした。"

        save_message(
            request.conversation_id,
            "ai",
            ai_message,
            deployment_name,
        )

        print("===== CHAT SUCCESS =====", flush=True)
        return {"reply": ai_message}

    except Exception as e:
        print(f"===== CHAT ERROR ===== {repr(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))