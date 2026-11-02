from fastapi import FastAPI

from pocket_wallet.router import router

app = FastAPI()
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}