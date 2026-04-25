from src.app.core.schemas.users import UserCreate, UserRead, TokenResponse, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from src.app.core.db.database import get_session
from fastapi import Depends
from src.app.repositories.users import UserRepository
from src.app.services.auth import AuthService

router = APIRouter(prefix="/users", tags=["users"])

def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(UserRepository(session))

@router.post("/register", response_model=UserRead, status_code=201)
async def register(
    data: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register(data)

@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(data)
