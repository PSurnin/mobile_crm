from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.app.core.db.database import get_session
from src.app.core.db.models.users import UserModel
from src.app.core.schemas.leads import BotLeadCreate, Lead, LeadCreate
from src.app.services.leads.leads_service import LeadService
from src.app.repositories.leads import LeadRepository
from src.app.core.config import settings

router = APIRouter(prefix="/bot", tags=["bot"])

async def verify_bot_secret(x_bot_secret: str = Header(...)):
    if x_bot_secret != settings.BOT_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid bot secret")


@router.post("/leads/", response_model=Lead, status_code=201)
async def create_lead_from_bot(
    data: BotLeadCreate,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(verify_bot_secret),
):
    # находим менеджера по invite_token
    result = await session.execute(
        select(UserModel).where(UserModel.invite_token == data.invite_token)
    )
    manager = result.scalar_one_or_none()

    if not manager:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    lead_data = LeadCreate(
        name=data.name,
        phone=data.phone,
        email=data.email,
    )

    service = LeadService(LeadRepository(session), manager.id)
    return await service.create_lead(lead_data, telegram_id=data.telegram_id)