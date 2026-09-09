from src.app.core.exceptions import EmailAlreadyRegistered, InvalidCredentials
from src.app.core.schemas.users import UserCreate, UserLogin, TokenResponse
from src.app.core.db.models.users import UserModel
from src.app.repositories.users import UserRepository
from src.app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate) -> UserModel:
        if await self.repo.get_by_email(data.email):
            raise EmailAlreadyRegistered()
        hashed_pwd = await hash_password(data.password)
        return await self.repo.create(data, hashed_pwd)


    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self.repo.get_by_email(data.email)
        if not user or not await verify_password(data.password, user.password_hash):
            raise InvalidCredentials()
        token = create_access_token(user.id, user.role.value)
        return TokenResponse(access_token=token)
