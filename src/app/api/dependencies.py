from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.db.database import get_session
from src.app.core.db.models.users import UserModel
from src.app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserModel:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await session.get(UserModel, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user