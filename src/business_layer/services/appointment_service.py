import datetime
import logging
from typing import Tuple, List

from src.business_layer.exception.security_exception import SecurityException
from src.business_layer.utils.validation import Validator
from src.data_layer.entities.appointment import Appointment
from src.data_layer.enum.appointment_status import AppointmentStatus
from src.data_layer.enum.appointment_type import AppointmentType
from src.data_layer.repository.appointment_repository import AppointmentRepository


class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()

    def create(self, data: dict) -> Tuple[bool, str, Appointment | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['member_id', 'gym_id', 'staff_id', 'appointment_type', 'schedule_date', 'duration']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not Validator.is_valid_datetime(data['schedule_date']):
                raise SecurityException("Invalid date format, date format is YYYY-MM-DD")
            else:
                data['schedule_date'] = datetime.datetime.strptime(data['schedule_date'], '%Y-%m-%d')

            if not isinstance(data['appointment_type'], AppointmentType):
                raise SecurityException("Invalid appointment type")

            if not isinstance(data['schedule_date'], datetime.datetime):
                raise SecurityException("Invalid schedule date format")

            try:
                data['duration'] = int(data['duration'])
            except ValueError:
                raise SecurityException("duration must be an integer")

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

            required_fields = ['member_id', 'gym_id','staff_id', 'appointment_type', 'schedule_date', 'duration',]
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['appointment_type'], AppointmentType):
                raise SecurityException("Invalid appointment type")

            if not Validator.is_valid_datetime(data['schedule_date']):
                raise SecurityException("Invalid date format, date format is YYYY-MM-DD")
            else:
                data['schedule_date'] = datetime.datetime.strptime(data['schedule_date'], '%Y-%m-%d')

            if not isinstance(data['schedule_date'], datetime.datetime):
                raise SecurityException("Invalid schedule date format")

            try:
                data['duration'] = int(data['duration'])
            except ValueError:
                raise SecurityException("duration must be an integer")

            if not isinstance(data['duration'], int) or data['duration'] <= 0:
                raise SecurityException("Duration must be a positive integer")


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

    def get_appointment_with_pending_payment_by_member_id(self, member_id : str) -> list[Appointment]:
        appointments = self.appointment_repository.get_all()
        return [appointment for appointment in appointments if appointment.member_id == member_id and not appointment.is_paid and appointment.status == AppointmentStatus.ACTIVE]

    def complete_payment_for_appointments_by_member_id(self, member_id : str):
        appointments = self.get_appointment_with_pending_payment_by_member_id(member_id)

        for appointment in appointments:
            self.appointment_repository.complete_payment(appointment.id)

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

    def cancel(self, _id: str) -> Tuple[bool, str]:
        try:
            if self.appointment_repository.get_by_id(_id) is None:
                raise SecurityException("No appointment exists with the given ID")

            self.appointment_repository.cancel(_id)
            return True, ""
        except SecurityException as e:
            logging.error(f"SecurityException occurred while cancelling appointment: {str(e)}")
            return False, str(e)
        except Exception as e:
            logging.error(f"Error occurred while cancelling appointment: {str(e)}")
            return False, str(e)

    def complete(self, _id: str) -> Tuple[bool, str]:
        try:
            appointment = self.appointment_repository.get_by_id(_id)

            if appointment is None:
                raise SecurityException("No appointment exists with the given ID")

            if not appointment.is_paid:
                raise SecurityException("Cannot complete appointment with pending payment")

            self.appointment_repository.complete(_id)
            return True, ""
        except SecurityException as e:
            logging.error(f"SecurityException occurred while completing appointment: {str(e)}")
            return False, str(e)
        except Exception as e:
            logging.error(f"Error occurred while completing appointment: {str(e)}")
            return False, str(e)
