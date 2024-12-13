import logging
from typing import Tuple, List

from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.entities.attendance import Attendance
from src.data_layer.repository.attendance_repository import AttendanceRepository


class AttendanceService:
    def __init__(self):
        self.attendance_repository = AttendanceRepository()

    def create(self, data: dict) -> Tuple[bool, str, Attendance | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['member_id' , 'gym_id', 'workout_zone_id', 'checkin_time', 'checkout_time']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

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

