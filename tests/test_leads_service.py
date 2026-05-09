import pytest
from fastapi import HTTPException
from src.app.core.schemas.leads import LeadCreate, LeadStatusUpdate, LeadStatus
from src.app.services.leads import leads_service as service

pytestmark = pytest.mark.asyncio

# TODO: upd tests to work with repositories instead of services

async def test_create_lead(session):
    data = LeadCreate(name="Иван", phone="+79991234567", email="ivan@test.com")
    lead = await service.create_lead(data, session)
    assert lead.id is not None
    assert lead.status == LeadStatus.new


async def test_get_leads_filter_by_status(session):
    await service.create_lead(LeadCreate(name="А", phone="1", email="a@test.com"), session)
    await service.create_lead(LeadCreate(name="Б", phone="2", email="b@test.com"), session)
    await service.update_lead_status(1, LeadStatusUpdate(status=LeadStatus.in_progress), session)

    result = await service.get_leads(session, status=LeadStatus.new)
    assert len(result) == 1
    assert result[0].name == "Б"


async def test_get_lead_by_id_not_found(session):
    with pytest.raises(HTTPException) as exc:
        await service.get_lead_by_id(999, session)
    assert exc.value.status_code == 404


async def test_update_lead_status(session):
    await service.create_lead(LeadCreate(name="В", phone="3", email="v@test.com"), session)
    lead = await service.update_lead_status(1, LeadStatusUpdate(status=LeadStatus.in_progress), session)
    assert lead.status == LeadStatus.in_progress


async def test_delete_lead(session):
    await service.create_lead(LeadCreate(name="Г", phone="4", email="g@test.com"), session)
    await service.delete_lead(1, session)

    with pytest.raises(HTTPException) as exc:
        await service.get_lead_by_id(1, session)
    assert exc.value.status_code == 404
