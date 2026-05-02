from src.app.core.schemas.leads import LeadCreate
from src.app.core.db.models.leads import LeadModel
from src.app.core.db.models.users import UserModel
from src.app.core.schemas.leads import LeadCreate, LeadStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class LeadRepository:
    def __init__(self, session: AsyncSession, current_user: UserModel):
        self.session = session
        self.current_user = current_user

    def _user_filter(self):
        return select(LeadModel).where(
            LeadModel.assigned_to == self.current_user.id
        )

    async def create_lead(self, data: LeadCreate) -> LeadModel:
        lead = LeadModel(status="new", assigned_to=self.current_user.id, **data.model_dump())
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)

        return lead

    async def get_by_id(self, id: int) -> LeadModel | None:
        query = self._user_filter().where(LeadModel.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, status: LeadStatus | None = None) -> list[LeadModel]:
        query = self._user_filter()
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