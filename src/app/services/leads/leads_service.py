import logging
from src.app.core.schemas.leads import LeadCreate, LeadStatus, LeadStatusUpdate
from src.app.services.leads.state_machine import can_transition
from src.app.core.db.models.leads import LeadModel
from src.app.repositories.leads import LeadRepository
from fastapi import HTTPException


logger = logging.getLogger(__name__)

class LeadService:
    def __init__(self, repo: LeadRepository, user_id: int):
        self.repo = repo
        self.user_id = user_id

    async def create_lead(self, data: LeadCreate, telegram_id: int | None = None,) -> LeadModel:
        return await self.repo.create_lead(data, self.user_id, telegram_id)

    async def get_leads(self, status: LeadStatus | None = None) -> list[LeadModel]:
        return await self.repo.get_all(self.user_id, status)

    async def get_lead_by_id(self, lead_id: int) -> LeadModel:
        lead = await self.repo.get_by_id(self.user_id, lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")
        return lead

    async def update_lead_status(self, lead_id: int, update: LeadStatusUpdate) -> LeadModel:
        lead = await self.repo.get_by_id(self.user_id, lead_id)
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
        return await self.repo.update_status(lead, update.status)

    async def delete_lead(self, lead_id: int) -> None:
        lead = await self.repo.get_by_id(self.user_id, lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")

        return await self.repo.delete(lead)
