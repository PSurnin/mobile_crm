import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.app.core.db.database import Base
import src.app.core.db.models  # для Base
from src.app.core.db.models.users import UserModel, UserRole
from src.app.repositories.leads import LeadRepository
from src.app.core.db.models.leads import LeadModel
from src.app.services.leads.leads_service import LeadService
from src.app.main import app
from src.app.core.db.database import get_session
from src.app.api.dependencies import get_current_user

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


@pytest_asyncio.fixture
async def async_client(session, test_user):
    # setup
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    # teardown
    app.dependency_overrides.clear()

@pytest.fixture
def make_lead(session, test_user):
    async def _make(**overrides):
        fields = {
            "name": "John",
            "phone": "911",
            "email": "john@test.com",
            "assigned_to": test_user.id,
        }
        fields.update(overrides) # точечное переопределение
        lead = LeadModel(**fields)
        session.add(lead)
        await session.commit()
        await session.refresh(lead)
        return lead
    return _make