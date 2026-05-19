from src.app.core.db.models.users import UserModel
from src.app.repositories.leads import LeadRepository
from src.app.core.schemas.leads import LeadCreate

async def test_get_by_id_wrong_user(session, test_user):
    """лид существует но принадлежит другому юзеру — должен вернуть None"""
    other_user = UserModel(name="Other", email="o@test.com", 
                           password_hash="h", invite_token="other-token")
    session.add(other_user)
    await session.commit()

    repo = LeadRepository(session)
    lead = await repo.create_lead(
        LeadCreate(name="X", phone="1", email="x@test.com"), 
        assigned_to=other_user.id
    )

    result = await repo.get_by_public_id(test_user.id, lead.public_id)
    assert result is None