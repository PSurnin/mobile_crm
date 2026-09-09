from src.app.core.db.models.users import UserModel
from src.app.core.schemas.users import InviteLink, UserRead
from fastapi import APIRouter
from fastapi import Depends
from src.app.api.dependencies import get_current_user
from src.app.core.config import settings

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/invite-link", response_model=InviteLink)
async def get_invite_link(
    current_user: UserModel = Depends(get_current_user),
) -> InviteLink:
    return InviteLink(url=f't.me/{settings.BOT_USERNAME}?start={current_user.invite_token}')

@router.get("/me", response_model=UserRead)
async def get_me(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    return current_user
