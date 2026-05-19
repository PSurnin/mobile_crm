from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.db.database import get_session
from src.app.core.schemas.leads import BotLeadCreate, Lead, LeadCreate
from src.app.services.leads.leads_service import LeadService
from src.app.repositories.leads import LeadRepository
from src.app.repositories.users import UserRepository
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
    user_repo = UserRepository(session)
    manager = user_repo.get_by_invite_token(data.invite_token)
    if not manager:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    lead_data = LeadCreate(
        name=data.name,
        phone=data.phone,
        email=data.email,
    )

    service = LeadService(LeadRepository(session), manager.id)
    return await service.create_lead(lead_data, telegram_id=data.telegram_id)
