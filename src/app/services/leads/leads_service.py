import logging
from src.app.core.schemas import LeadCreate, Lead, LeadStatus, LeadStatusUpdate
from src.app.services.leads.state_machine import can_transition
from src.app.core.db.models import LeadModel
from src.app.core.db.database import get_session
from fastapi import HTTPException, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_fake_db = []
_id_counter = 1

# TODO: LeadService - class based service/view - calls Repository
# TODO: LeadRepository - all things about DB and model interaction

async def create_lead(
    data: LeadCreate,
    session: AsyncSession,
) -> Lead:
    lead = LeadModel(status="new", **data.model_dump())
    session.add(lead)
    await session.commit()
    await session.refresh(lead)
    logger.info(f"New lead created: {lead}")

    return lead

async def get_leads(
    session: AsyncSession,
    status: LeadStatus | None = None,
) -> list[Lead]:
    query = select(LeadModel)

    if status:
        query = query.where(LeadModel.status == status)

    result = await session.execute(query)
    return result.scalars().all()

async def get_lead_by_id(
    lead_id: int,
    session: AsyncSession,
) -> Lead:
    result = await session.execute(
        select(LeadModel).where(LeadModel.id == lead_id)
    )
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")
    return lead

async def update_lead_status(
    lead_id: int,
    update: LeadStatusUpdate,
    session: AsyncSession,
) -> Lead:
    result = await session.execute(
        select(LeadModel).where(LeadModel.id == lead_id)
    )
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")

    if update.status == lead.status:
        raise HTTPException(
            status_code=400,
            detail=f"Lead already has status '{lead.status}'"
        )

    if not can_transition(lead.status, update.status):
        raise HTTPException(
            status_code=422,
            detail=(
                f"Cannot transition from '{lead.status}' to '{update.status}'. "
            )
        )

    lead.status = update.status

    await session.commit()
    await session.refresh(lead)

    logger.info(f"Lead {lead_id} status: {lead.status} → {update.status}")
    return lead

async def delete_lead(
    lead_id: int,
    session: AsyncSession,
) -> None:
        result = await session.execute(
            select(LeadModel).where(LeadModel.id == lead_id)
        )
        lead = result.scalar_one_or_none()

        if not lead:
            raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")
        await session.execute(
            delete(lead)
        )
        await session.commit()
        logger.info(f"Lead {lead_id} deleted")
