from src.app.core.schemas.leads import LeadStatus

class DomainError(Exception):
    """ Business rules exceptions """

class LeadNotFound(DomainError):
    def __init__(self, public_id: str):
        self.public_id = public_id 
        super().__init__(f"Lead {public_id} not found")

class LeadStatusError(DomainError):
    def __init__(self, lead_status: LeadStatus):
        self.lead_status = lead_status 
        super().__init__(f"Lead already has status '{lead_status.value}'")

class InvalidStatusTransition(DomainError):
    def __init__(self, lead_status: LeadStatus, update_status: LeadStatus):
        self.lead_status = lead_status
        self.update_status = update_status 
        super().__init__(f"Cannot transition from '{lead_status.value}' to '{update_status.value}'.")

class EmailAlreadyRegistered(DomainError):
    def __init__(self):
        super().__init__("Email already registered")

class InvalidCredentials(DomainError):
    def __init__(self):
        super().__init__("Invalid credentials")

class RequiredFieldMissing(DomainError):
    def __init__(self, field: str, status: LeadStatus):
        self.field = field
        self.status = status
        super().__init__(f"'{field}' is required to move a lead to '{status.value}'")