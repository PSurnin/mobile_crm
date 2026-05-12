from fastapi import APIRouter
from src.app.core.schemas.leads import LeadCreate, Lead, LeadStatusUpdate, LeadStatus
from src.app.services.leads.leads_service import LeadService
from src.app.repositories.leads import LeadRepository
from src.app.core.db.database import get_session
from src.app.api.dependencies import get_current_user
from src.app.core.db.models.users import UserModel
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/leads", tags=["leads"])


def get_lead_service(
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> LeadService:
    return LeadService(LeadRepository(session), current_user.id)

@router.post("/add", response_model=Lead)
async def create_lead(
    data: LeadCreate,
    service: LeadService = Depends(get_lead_service),
):
    return await service.create_lead(data)

@router.get("/get/{lead_id}", response_model=Lead)
async def get_lead(
    lead_id: str,
    service: LeadService = Depends(get_lead_service),
):
    return await service.get_lead_by_id(lead_id)

@router.get("/list", response_model=list[Lead])
async def list_leads(
    status: LeadStatus | None = None,
    service: LeadService = Depends(get_lead_service),
):
    return await service.get_leads(status=status)

@router.patch("/update/{lead_id}/status", response_model=Lead)
async def update_lead_status(
    lead_id: int,
    update: LeadStatusUpdate,
    service: LeadService = Depends(get_lead_service),
):
    return await service.update_lead_status(lead_id, update)

@router.delete("/delete/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service),
):
    await service.delete_lead(lead_id)
