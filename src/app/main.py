import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from src.app.api import router
from src.app.api.error_handlers import register_error_handlers
from src.app.core.db.database import engine
from src.app.core.logging import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    yield
    # --- shutdown ---
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        process_time = time.perf_counter() - start_time
        status = response.status_code if response is not None else "ERROR"
        logger.info("%s %s -> %s (%.4fs)", request.method, request.url.path, status, process_time)
        if response is not None:
            response.headers["X-Process-Time"] = str(process_time)

app.include_router(router)
register_error_handlers(app)

@app.get("/")
def root():
    return {"message": "Mini CRM API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
