import logging
import datetime
from typing import Tuple, List

from src.data_layer.entities.appointment import Appointment
from src.data_layer.enum.appointment_status import AppointmentStatus
from src.data_layer.enum.appointment_type import AppointmentType
from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.repository.appointment_repository import AppointmentRepository


class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()

    def create(self, data: dict) -> Tuple[bool, str, Appointment | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['member_id', 'staff_id', 'appointment_type', 'schedule_date', 'duration']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['appointment_type'], AppointmentType):
                raise SecurityException("Invalid appointment type")

            if not isinstance(data['schedule_date'], datetime.datetime):
                raise SecurityException("Invalid schedule date format")

            if not isinstance(data['duration'], int) or data['duration'] <= 0:
                raise SecurityException("Duration must be a positive integer")

            appointment = self.appointment_repository.create(data)
            return True, "", appointment
        except SecurityException as e:
            logging.error(f"SecurityException occurred while creating appointment: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while creating appointment: {str(e)}")
            return False, str(e), None

    def update(self, _id: str, data: dict) -> Tuple[bool, str, Appointment | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['member_id', 'staff_id', 'appointment_type', 'schedule_date', 'duration', 'status']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['appointment_type'], AppointmentType):
                raise SecurityException("Invalid appointment type")

            if not isinstance(data['schedule_date'], datetime.datetime):
                raise SecurityException("Invalid schedule date format")

            if not isinstance(data['duration'], int) or data['duration'] <= 0:
                raise SecurityException("Duration must be a positive integer")

            if not isinstance(data['status'], AppointmentStatus):
                raise SecurityException("Invalid appointment status")

            if self.appointment_repository.get_by_id(_id) is None:
                raise SecurityException("No appointment exists with the given ID")

            appointment = self.appointment_repository.update(_id, data)
            return True, "", appointment
        except SecurityException as e:
            logging.error(f"SecurityException occurred while updating appointment: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while updating appointment: {str(e)}")
            return False, str(e), None

    def get_all(self) -> List[Appointment]:
        return self.appointment_repository.get_all()

    def get_by_id(self, _id: str) -> Tuple[bool, str, Appointment | None]:
        try:
            appointment = self.appointment_repository.get_by_id(_id)

            if appointment is None:
                raise SecurityException("No appointment exists with the given ID")

            return True, "", appointment
        except SecurityException as e:
            logging.error(f"SecurityException occurred while retrieving appointment: {str(e)}")
            return False, str(e), None

    def delete(self, _id: str) -> Tuple[bool, str]:
        try:
            if self.appointment_repository.get_by_id(_id) is None:
                raise SecurityException("No appointment exists with the given ID")

            self.appointment_repository.delete(_id)
            return True, ""
        except SecurityException as e:
            logging.error(f"SecurityException occurred while deleting appointment: {str(e)}")
            return False, str(e)
        except Exception as e:
            logging.error(f"Error occurred while deleting appointment: {str(e)}")
            return False, str(e)
