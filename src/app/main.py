from fastapi import FastAPI
from src.app.api import router
from src.app.core.db.database import engine, Base

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Mini CRM API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
