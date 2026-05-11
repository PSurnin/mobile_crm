import httpx
from src.tg_bot.config import settings

API_URL = "http://localhost:8000"


async def create_lead(
    invite_token: str,
    name: str,
    phone: str,
    email: str,
    telegram_id: int,
) -> dict | None:
    async with httpx.AsyncClient() as client:
        try:
            # TODO: API endpoint in main app
            response = await client.post(
                f"{API_URL}/bot/leads/",
                json={
                    "invite_token": invite_token,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "telegram_id": telegram_id,
                },
                headers={"x-bot-secret": settings.BOT_SECRET_KEY},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return None
