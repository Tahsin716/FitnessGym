from enum import Enum


class AppointmentStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"