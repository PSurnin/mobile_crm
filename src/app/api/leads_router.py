from fastapi import APIRouter
from src.app.core.schemas import LeadCreate, Lead, LeadStatusUpdate, LeadStatus
from src.app.services.leads import leads_service

lead_router = APIRouter(prefix="/leads", tags=["leads"])

@lead_router.post("/add", response_model=Lead)
def create_lead_endpoint(data: LeadCreate):
    return leads_service.create_lead(data)

@lead_router.get("/get/{lead_id}", response_model=Lead)
def get_lead_endpoint(lead_id: int):
    return leads_service.get_lead_by_id(lead_id)

@lead_router.get("/list", response_model=list[Lead])
def list_leads(status: LeadStatus | None = None):
    return leads_service.get_leads(status=status)

@lead_router.patch("/update/{lead_id}/status", response_model=Lead)
def update_lead_status(lead_id: int, update: LeadStatusUpdate):
    return leads_service.update_lead_status(lead_id, update)

@lead_router.delete("/delete/{lead_id}", status_code=204)
def delete_lead(lead_id: int):
    leads_service.delete_lead(lead_id)