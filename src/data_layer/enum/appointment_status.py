from enum import Enum


class AppointmentStatus(Enum):
    ACTIVE = "Active"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"