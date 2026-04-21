from fastapi import FastAPI
from src.app.api.leads_router import lead_router

app = FastAPI()

app.include_router(lead_router)

@app.get("/")
def root():
    return {"message": "Mini CRM API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
