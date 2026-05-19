import pytest
from fastapi import HTTPException
from src.app.core.schemas.leads import LeadCreate, LeadStatusUpdate, LeadStatus


async def test_create_lead(lead_service):
    data = LeadCreate(name="Иван", phone="+79991234567", email="ivan@test.com")
    lead = await lead_service.create_lead(data)
    assert lead.id is not None
    assert lead.status == LeadStatus.new


async def test_get_leads_filter_by_status(lead_service):
    first_lead = await lead_service.create_lead(LeadCreate(name="А", phone="1", email="a@test.com"))
    await lead_service.create_lead(LeadCreate(name="Б", phone="2", email="b@test.com"))
    await lead_service.update_lead_status(first_lead.public_id, LeadStatusUpdate(status=LeadStatus.in_progress))

    result = await lead_service.get_leads(status=LeadStatus.new)
    assert len(result) == 1
    assert result[0].name == "Б"


async def test_get_lead_by_id_not_found(lead_service):
    with pytest.raises(HTTPException) as exc:
        await lead_service.get_lead_or_404(999)
    assert exc.value.status_code == 404


async def test_update_lead_status(lead_service):
    lead = await lead_service.create_lead(LeadCreate(name="В", phone="3", email="v@test.com"))
    await lead_service.update_lead_status(lead.public_id, LeadStatusUpdate(status=LeadStatus.in_progress))
    assert lead.status == LeadStatus.in_progress


async def test_delete_lead(lead_service):
    lead = await lead_service.create_lead(LeadCreate(name="Г", phone="4", email="g@test.com"))
    await lead_service.delete_lead(lead.public_id)

    with pytest.raises(HTTPException) as exc:
        await lead_service.get_lead_or_404(lead.public_id)
    assert exc.value.status_code == 404
