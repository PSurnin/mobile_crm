import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from src.app.core.exceptions import (
    LeadNotFound, LeadStatusError, InvalidStatusTransition,
    EmailAlreadyRegistered, InvalidCredentials,
)

logger = logging.getLogger(__name__)

async def lead_not_found_handler(request: Request, exc: LeadNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Lead {exc.public_id} not found"},
    )

async def invalid_lead_status_handler(request: Request, exc: LeadStatusError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"Lead already has status '{exc.lead_status.value}'"},
    )

async def invalid_transition_handler(request: Request, exc: InvalidStatusTransition) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": f"Cannot transition from '{exc.lead_status.value}' to '{exc.update_status.value}'."},
    )

async def invalid_email_handler(request: Request, exc: EmailAlreadyRegistered) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Email already registered"},
    )

async def invalid_credentials_handler(request: Request, exc: InvalidCredentials) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid credentials"},
    )

async def db_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("DB error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(LeadNotFound, lead_not_found_handler)
    app.add_exception_handler(LeadStatusError, invalid_lead_status_handler)
    app.add_exception_handler(InvalidStatusTransition, invalid_transition_handler)
    app.add_exception_handler(EmailAlreadyRegistered, invalid_email_handler)
    app.add_exception_handler(InvalidCredentials, invalid_credentials_handler)
    app.add_exception_handler(SQLAlchemyError, db_error_handler)
