from src.app.core.schemas.leads import LeadStatus

LEAD_TRANSITIONS: dict[LeadStatus, list[LeadStatus]] = {
    LeadStatus.new: [LeadStatus.in_progress],
    LeadStatus.in_progress: [LeadStatus.closed],
    LeadStatus.closed: [],
}

def can_transition(current: LeadStatus, new: LeadStatus) -> bool:
    return new in LEAD_TRANSITIONS.get(current, [])