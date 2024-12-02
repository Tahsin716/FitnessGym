from typing import Dict, List, cast
from src.data_layer.entities.attendance import Attendance


class AttendanceRepository:
    _instance: "AttendanceRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__attendances = cast(Dict[str, Attendance], {})
        return cls._instance

    def create(self, data: dict) -> Attendance:
        attendance = Attendance(data)
        self.__attendances[attendance.id] = attendance
        return attendance

    def get_all(self) -> List[Attendance]:
        return list(self.__attendances.values())

