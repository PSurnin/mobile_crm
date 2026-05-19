from src.app.core.schemas.users import UserCreate
from src.app.core.db.models.users import UserModel
from src.app.core.utils import generate_public_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate, password_hash: str) -> UserModel:
        user = UserModel(
            name=data.name,
            email=data.email,
            password_hash=password_hash,
            invite_token=generate_public_token(),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_invite_token(self, invite_token: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.invite_token == invite_token)
        )
        return result.scalar_one_or_none()
