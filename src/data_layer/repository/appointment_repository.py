from typing import Dict, List, cast

from src.data_layer.entities.appointment import Appointment
from src.data_layer.enum.appointment_status import AppointmentStatus


class AppointmentRepository:
    _instance: "AppointmentRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__appointments = cast(Dict[str, Appointment], {})
        return cls._instance

    def create(self, data: dict) -> Appointment:
        appointment = Appointment(data)
        self.__appointments[appointment.id] = appointment
        return appointment

    def update(self, _id: str, data: dict) -> Appointment:
        appointment = self.__appointments[_id]
        appointment.member_id = data["member_id"]
        appointment.gym_id = data["gym_id"]
        appointment.staff_id = data["staff_id"]
        appointment.appointment_type = data["appointment_type"]
        appointment.scheduled_date = data["schedule_date"]
        appointment.duration = data["duration"]
        return appointment

    def get_all(self) -> List[Appointment]:
        return list(self.__appointments.values())

    def get_by_id(self, _id: str) -> Appointment:
        return self.__appointments.get(_id)

    def delete(self, _id: str) -> None:
        if _id in self.__appointments:
            del self.__appointments[_id]

    def cancel(self, _id: str) -> None:
        if _id in self.__appointments:
            appointment = self.__appointments[_id]
            appointment.status = AppointmentStatus.CANCELLED

    def complete(self, _id: str) -> None:
        if _id in self.__appointments:
            appointment = self.__appointments[_id]
            appointment.status = AppointmentStatus.COMPLETED

    def complete_payment(self, _id: str) -> None:
        if _id in self.__appointments:
            appointment = self.__appointments[_id]
            appointment.is_paid = True