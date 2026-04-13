from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}

@app.get("/debug-ping")
def debug_ping():
    return {"ok": True}

