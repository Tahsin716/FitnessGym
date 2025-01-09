import datetime

from src.business_layer.providers.appointment_info_provider import AppointmentProvider
from src.data_layer.entities.base_entity import BaseEntity
from src.data_layer.enum.appointment_status import AppointmentStatus
from src.data_layer.enum.appointment_type import AppointmentType


class Appointment(BaseEntity):
    def __init__(self, data : dict):
        _id = data.get('_id', None)
        create_date = data.get('create_date', None)
        super().__init__(_id, create_date)

        self.__member_id : str = data['member_id']
        self.__gym_id : str = data['gym_id']
        self.__staff_id : str = data['staff_id']
        self.__appointment_type : AppointmentType = data['appointment_type']
        self.__scheduled_date : datetime = data['schedule_date']
        self.__status : AppointmentStatus = AppointmentStatus.ACTIVE
        self.__duration : int = data['duration']
        self.__cost : float = self.__calculate_session_cost()
        self.__is_paid : bool = data.get('is_paid', False)

    @property
    def gym_id(self) -> str:
        return self.__gym_id

    @gym_id.setter
    def gym_id(self, value : str):
        self.__gym_id = value

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
        self.__cost = self.__calculate_session_cost()

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
        self.__cost = self.__calculate_session_cost()

    @property
    def cost(self) -> float:
        return self.__cost

    @property
    def is_paid(self) -> bool:
        return self.__is_paid

    @is_paid.setter
    def is_paid(self, value : bool):
        self.__is_paid = value

    def __calculate_session_cost(self) -> float:
        return (self.__duration / 30) * AppointmentProvider.APPOINTMENT_COST_PER_SESSION[self.__appointment_type.value]