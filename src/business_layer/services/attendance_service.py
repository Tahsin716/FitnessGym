import logging
from datetime import datetime
from typing import Tuple, List

from src.business_layer.exception.security_exception import SecurityException
from src.business_layer.utils.common import Common
from src.business_layer.utils.validation import Validator
from src.data_layer.entities.attendance import Attendance
from src.data_layer.repository.attendance_repository import AttendanceRepository


class AttendanceService:
    def __init__(self):
        self.attendance_repository = AttendanceRepository()

    def create(self, data: dict) -> Tuple[bool, str, Attendance | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['member_id' , 'gym_id', 'zone_id', 'checkin_time', 'checkout_time']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not Validator.is_valid_time_format(data['checkin_time']) or not Validator.is_valid_time_format(data['checkout_time']):
                raise SecurityException("Invalid time format. Use HH:MM")

            if datetime.strptime(data['checkin_time'], "%H:%M") >= datetime.strptime(data['checkout_time'], "%H:%M"):
                raise SecurityException("Checkout time must be after checkin time")

            data['duration'] = Common.calculate_duration(data['checkin_time'], data['checkout_time'])

            if data['duration'] <= 0:
                raise SecurityException("Duration cannot be negative or 0")

            attendance = self.attendance_repository.create(data)
            return True, "", attendance
        except SecurityException as e:
            logging.error(f"SecurityException occurred while creating attendance: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while creating attendance: {str(e)}")
            return False, str(e), None

    def get_all(self) -> List[Attendance]:
        return self.attendance_repository.get_all()

