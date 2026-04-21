# tests/test_leads_service.py
import pytest
from src.app.core.schemas import LeadCreate, LeadStatusUpdate
from src.app.services.leads import leads_service


@pytest.fixture(autouse=True)
def clear_db():
    """Очищаем fake_db перед каждым тестом"""
    leads_service._fake_db.clear()
    leads_service._id_counter = 1
    yield


def test_create_lead():
    data = LeadCreate(name="Иван", phone="+79991234567", email="ivan@test.com")
    lead = leads_service.create_lead(data)
    assert lead.id == 1
    assert lead.status == "new"


def test_get_leads_filter_by_status():
    leads_service.create_lead(LeadCreate(name="А", phone="1", email="a@test.com"))
    leads_service.create_lead(LeadCreate(name="Б", phone="2", email="b@test.com"))
    leads_service.update_lead_status(1, LeadStatusUpdate(status="in_progress"))

    result = leads_service.get_leads(status="new")
    assert len(result) == 1
    assert result[0].name == "Б"


def test_get_lead_by_id_not_found():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        leads_service.get_lead_by_id(999)
    assert exc.value.status_code == 404


def test_update_lead_status():
    leads_service.create_lead(LeadCreate(name="В", phone="3", email="v@test.com"))
    updated = leads_service.update_lead_status(1, LeadStatusUpdate(status="in_progress"))
    assert updated.status == "in_progress"


def test_delete_lead():
    leads_service.create_lead(LeadCreate(name="Г", phone="4", email="g@test.com"))
    leads_service.delete_lead(1)
    assert leads_service.get_leads() == []