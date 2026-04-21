import logging
from src.app.core.schemas import LeadCreate, Lead, LeadStatus, LeadStatusUpdate
from src.app.services.leads.state_machine import can_transition
from fastapi import HTTPException

logger = logging.getLogger(__name__)

_fake_db = []
_id_counter = 1

def create_lead(data: LeadCreate) -> Lead:
    global _id_counter

    lead = Lead(id=_id_counter, status="new", **data.model_dump())

    _fake_db.append(lead)
    _id_counter += 1

    logger.info(f"New lead created: {lead}")

    return lead

def get_leads(status: LeadStatus | None = None) -> list[Lead]:
    if status is None:
        return _fake_db
    return [lead for lead in _fake_db if lead.status == status]

def get_lead_by_id(lead_id: int) -> Lead:
    for lead in _fake_db:
        if lead.id == lead_id:
            return lead
    raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")

def update_lead_status(lead_id: int, update: LeadStatusUpdate) -> Lead:
    lead = get_lead_by_id(lead_id)

    if update.status == lead.status:
        raise HTTPException(
            status_code=400,
            detail=f"Lead already has status '{lead.status}'"
        )

    if not can_transition(lead.status, update.status):
        raise HTTPException(
            status_code=422,
            detail=(
                f"Cannot transition from '{lead.status}' to '{update.status}'. "
            )
        )

    # Pydantic v2: модели иммутабельны по умолчанию, пересоздаём
    index = _fake_db.index(lead)
    updated = lead.model_copy(update={"status": update.status})
    _fake_db[index] = updated

    logger.info(f"Lead {lead_id} status: {lead.status} → {update.status}")
    return updated

def delete_lead(lead_id: int) -> None:
    lead = get_lead_by_id(lead_id)
    _fake_db.remove(lead)
    logger.info(f"Lead {lead_id} deleted")
