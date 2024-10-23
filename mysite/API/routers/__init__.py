from .users import user_router
from .services import service_router
from .medics import medic_router
from .medic_schedules import schedule_router
from .locations import location_router
from .appointments import appointment_router
from .consultations import consultation_router
from .departments import department_router

__all__ = [
    'user_router',
    'service_router',
    'medic_router',
    'location_router',
    'appointment_router',
    'consultation_router',
    'department_router',
    'schedule_router'
]