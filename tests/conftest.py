import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.app.core.db.database import Base
import src.app.core.db.models  # для Base
from src.app.core.db.models.users import UserModel, UserRole
from src.app.repositories.leads import LeadRepository
from src.app.services.leads.leads_service import LeadService

@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as s:
        yield s

    await engine.dispose()

@pytest_asyncio.fixture
async def test_user(session) -> UserModel:
    user = UserModel(
        name="Test Manager",
        email="manager@test.com",
        password_hash="hash",
        role=UserRole.manager,
        invite_token="test-token-123",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@pytest_asyncio.fixture
async def lead_service(session, test_user) -> LeadService:
    return LeadService(LeadRepository(session), test_user.id)
