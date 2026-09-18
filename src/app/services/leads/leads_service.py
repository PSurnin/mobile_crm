from datetime import datetime, timezone
import logging

from src.app.core.exceptions import LeadStatusError, LeadNotFound, InvalidStatusTransition, RequiredFieldMissing
from src.app.core.schemas.leads import LeadCreate, LeadStatus, LeadStatusUpdate
from src.app.services.leads.state_machine import can_transition
from src.app.core.db.models.leads import LeadModel
from src.app.repositories.leads import LeadRepository


logger = logging.getLogger(__name__)

class LeadService:
    def __init__(self, repo: LeadRepository, user_id: int):
        self.repo = repo
        self.user_id = user_id

    async def create_lead(self, data: LeadCreate, telegram_id: int | None = None,) -> LeadModel:
        return await self.repo.create_lead(data, self.user_id, telegram_id)

    async def get_leads(
            self,
            limit: int,
            offset: int,
            status: LeadStatus | None = None,
        ) -> list[LeadModel]:
        return await self.repo.get_all(self.user_id, limit, offset, status)

    async def get_lead_or_404(self, public_id: str) -> LeadModel:
        lead = await self.repo.get_by_public_id(self.user_id, public_id)
        if not lead:
            raise LeadNotFound(public_id)
        return lead

    async def update_lead_status(self, public_id: str, update: LeadStatusUpdate) -> LeadModel:
        lead = await self.get_lead_or_404(public_id)

        if update.status == lead.status:
            raise LeadStatusError(lead.status)

        if not can_transition(lead.status, update.status):
            raise InvalidStatusTransition(lead.status, update.status)

        if update.status == LeadStatus.in_progress:
            lead.contacted_at = datetime.now(timezone.utc)
        else:
            if update.status == LeadStatus.won:
                if update.amount is None:
                    raise RequiredFieldMissing("amount", LeadStatus.won)
                lead.amount = update.amount

            if update.status == LeadStatus.lost:
                if update.lost_reason is None:
                    raise RequiredFieldMissing("lost_reason", LeadStatus.lost)
                lead.lost_reason = update.lost_reason
            lead.closed_at = datetime.now(timezone.utc)

        lead.status = update.status

        return await self.repo.update(lead)

    async def delete_lead(self, public_id: str) -> None:
        lead = await self.get_lead_or_404(public_id)

        return await self.repo.delete(lead)
