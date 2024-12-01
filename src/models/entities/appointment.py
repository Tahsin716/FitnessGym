import datetime

from src.models.entities.base_entity import BaseEntity
from src.models.enum.appointment_status import AppointmentStatus
from src.models.enum.appointment_type import AppointmentType


class Appointment(BaseEntity):
    def __init__(self, data : dict):
        super().__init__()
        self.__member_id : str = data['member_id']
        self.__staff_id : str = data['staff_id']
        self.__appointment_type : AppointmentType = data['appointment_type']
        self.__scheduled_date : datetime = data['schedule_date']
        self.__status : AppointmentStatus = AppointmentStatus.ACTIVE
        self.__duration : int = data['duration']

    @property
    def member_id(self) -> str:
        return self.__member_id

    @member_id.setter
    def member_id(self, value: str) -> None:
        self.__member_id = value

    @property
    def staff_id(self) -> str:
        return self.__staff_id

    @staff_id.setter
    def staff_id(self, value: str) -> None:
        self.__staff_id = value

    @property
    def appointment_type(self) -> AppointmentType:
        return self.__appointment_type

    @appointment_type.setter
    def appointment_type(self, value: AppointmentType) -> None:
        self.__appointment_type = value

    @property
    def scheduled_date(self) -> datetime:
        return self.__scheduled_date

    @scheduled_date.setter
    def scheduled_date(self, value: datetime) -> None:
        self.__scheduled_date = value

    @property
    def status(self) -> AppointmentStatus:
        return self.__status

    @status.setter
    def status(self, value: AppointmentStatus) -> None:
        self.__status = value

    @property
    def duration(self) -> int:
        return self.__duration

    @duration.setter
    def duration(self, value: int) -> None:
        self.__duration = value