from fastapi import APIRouter
from src.app.core.schemas import LeadCreate, Lead, LeadStatusUpdate, LeadStatus
from src.app.services.leads import leads_service
from src.app.core.db.database import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

lead_router = APIRouter(prefix="/leads", tags=["leads"])

@lead_router.post("/add", response_model=Lead)
async def create_lead_endpoint(
    data: LeadCreate,
    session: AsyncSession = Depends(get_session),
):
    return await leads_service.create_lead(data, session)

@lead_router.get("/get/{lead_id}", response_model=Lead)
async def get_lead_endpoint(
    lead_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await leads_service.get_lead_by_id(lead_id, session)

@lead_router.get("/list", response_model=list[Lead])
async def list_leads(
    status: LeadStatus | None = None, 
    session: AsyncSession = Depends(get_session),
):
    return await leads_service.get_leads(session, status=status)

@lead_router.patch("/update/{lead_id}/status", response_model=Lead)
async def update_lead_status(
    lead_id: int,
    update: LeadStatusUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await leads_service.update_lead_status(lead_id, update, session)

@lead_router.delete("/delete/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    session: AsyncSession = Depends(get_session),
):
    await leads_service.delete_lead(lead_id, session)