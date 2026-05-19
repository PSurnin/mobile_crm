from src.app.core.db.models.leads import LeadModel
from src.app.core.schemas.leads import LeadCreate, LeadStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class LeadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _user_filter(self, user_id: int):
        return select(LeadModel).where(
            LeadModel.assigned_to == user_id
        )

    async def create_lead(
        self,
        data: LeadCreate,
        assigned_to: int,
        telegram_id: int | None = None,
    ) -> LeadModel:
        lead = LeadModel(
            status="new",
            assigned_to=assigned_to,
            telegram_id=telegram_id,
            **data.model_dump(),
        )
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)

        return lead

    async def get_by_public_id(self, assigned_to: int, public_id: str) -> LeadModel | None:
        query = self._user_filter(assigned_to).where(LeadModel.public_id == public_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, assigned_to:int, status: LeadStatus | None = None) -> list[LeadModel]:
        query = self._user_filter(assigned_to)
        if status:
            query = query.where(LeadModel.status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_status(self, lead: LeadModel, new_status: LeadStatus) -> LeadModel:
        lead.status = new_status
        await self.session.commit()
        await self.session.refresh(lead)
        return lead

    async def delete(self, lead: LeadModel) -> None:
        await self.session.delete(lead)
        await self.session.commit()