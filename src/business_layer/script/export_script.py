import json
import logging
import os
from datetime import datetime
from typing import Tuple

from src.business_layer.providers.config import Config
from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.attendance_service import AttendanceService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.payment_service import PaymentService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.business_layer.services.subscription_service import SubscriptionService
from src.business_layer.services.zone_service import ZoneService


class ExportScript:
    def __init__(self):
        self.__gym_service = GymService()
        self.__staff_member_service = StaffMemberService()
        self.__zone_service = ZoneService()
        self.__gym_member_service = GymMemberService()
        self.__appointment_service = AppointmentService()
        self.__subscription_service = SubscriptionService()
        self.__payment_service = PaymentService()
        self.__attendance_service = AttendanceService()
        self.__export_data = {}

    def export(self) -> Tuple[bool, str]:
        try:
            self.__export_gyms()
            self.__export_zones()
            self.__export_gym_members()
            self.__export_staff()
            self.__export_payments()
            self.__export_subscription()
            self.__export_appointments()
            self.__export_attendances()
            self.__write_to_file()
            message = "Successfully exported all data"
            logging.info(message)
            return True, message
        except Exception as e:
            message = f"Export failed: {str(e)}"
            logging.error(message)
            return False, message

    def __export_gyms(self):
        gyms = self.__gym_service.get_all_gyms()
        self.__export_data["Gyms"] = []

        for gym in gyms:
            data = {
                "_id": gym.id,
                "create_date": gym.create_date,
                "location": gym.location,
                "address": gym.address,
                "post_code": gym.post_code,
                "phone_number": gym.phone_number,
                "email": gym.email
            }
            self.__export_data["Gyms"].append(data)

        logging.info(f"Exported {len(gyms)} gyms")

    def __export_staff(self):
        staffs = self.__staff_member_service.get_all()
        self.__export_data["StaffMembers"] = []

        for staff in staffs:
            data = {
                "_id": staff.id,
                "create_date": staff.create_date,
                "first_name": staff.first_name,
                "last_name": staff.last_name,
                "email": staff.email,
                "phone_number": staff.phone_number,
                "role": staff.role.value,
                "gym_id": staff.gym_id
            }
            self.__export_data["StaffMembers"].append(data)

        logging.info(f"Exported {len(staffs)} staff members")

    def __export_zones(self):
        zones = self.__zone_service.get_all_zones()
        self.__export_data["Zones"] = []

        for zone in zones:
            data = {
                "_id": zone.id,
                "create_date": zone.create_date,
                "gym_id": zone.gym_id,
                "zone_type": zone.zone_type.value,
                "attendant_id": zone.attendant_id
            }
            self.__export_data["Zones"].append(data)

        logging.info(f"Exported {len(zones)} zones")

    def __export_gym_members(self):
        members = self.__gym_member_service.get_all()
        self.__export_data["GymMembers"] = []

        for member in members:
            data = {
                "_id": member.id,
                "create_date": member.create_date,
                "first_name": member.first_name,
                "last_name": member.last_name,
                "email": member.email,
                "phone_number": member.phone_number,
                "membership_type": member.membership_type.value,
                "height": member.height,
                "weight": member.weight
            }
            self.__export_data["GymMembers"].append(data)

        logging.info(f"Exported {len(members)} gym members")

    def __export_appointments(self):
        appointments = self.__appointment_service.get_all()
        self.__export_data["Appointments"] = []

        for appointment in appointments:
            data = {
                "_id": appointment.id,
                "create_date": appointment.create_date,
                "member_id": appointment.member_id,
                "gym_id": appointment.gym_id,
                "staff_id": appointment.staff_id,
                "appointment_type": appointment.appointment_type.value,
                "schedule_date": appointment.scheduled_date,
                "status": appointment.status.value,
                "duration": appointment.duration,
                "is_paid": appointment.is_paid
            }
            self.__export_data["Appointments"].append(data)

    def __export_subscription(self):
        subscriptions = self.__subscription_service.get_all()
        self.__export_data["Subscriptions"] = []

        for subscription in subscriptions:
            data = {
                "_id": subscription.id,
                "create_date": subscription.create_date,
                "member_id": subscription.member_id,
                "subscription_plan": subscription.subscription_plan.value,
                "payment_method": subscription.payment_method.value,
                "discount": subscription.discount,
                "active": subscription.active,
                "loyalty_points": subscription.loyalty_points
            }
            self.__export_data["Subscriptions"].append(data)

    def __export_payments(self):
        payments = self.__payment_service.get_all()
        self.__export_data["Payments"] = []

        for payment in payments:
            data = {
                "_id": payment.id,
                "create_date": payment.create_date,
                "member_id": payment.member_id,
                "subscription_plan": payment.subscription_plan.value,
                "appointment_ids": payment.appointment_ids,
                "payment_method": payment.payment_method.value,
                "amount": payment.amount
            }
            self.__export_data["Payments"].append(data)

    def __export_attendances(self):
        attendances = self.__attendance_service.get_all()
        self.__export_data["Attendances"] = []

        for attendance in attendances:
            data = {
                "_id": attendance.id,
                "create_date": attendance.create_date,
                "member_id": attendance.member_id,
                "gym_id": attendance.gym_id,
                "zone_id": attendance.zone_id,
                "checkin_time": attendance.checkin_time,
                "checkout_time": attendance.checkout_time,
                "duration": attendance.duration
            }
            self.__export_data["Attendances"].append(data)

    def _make_serializable(self, data):
        if isinstance(data, datetime):
            return str(data.strftime("%Y-%m-%d"))
        elif isinstance(data, list):
            return [self._make_serializable(item) for item in data]
        elif isinstance(data, dict):
            return {key: self._make_serializable(value) for key, value in data.items()}
        else:
            return data

    def __write_to_file(self):

        file_path = os.path.join(Config.DB_PATH, Config.DB_NAME)

        os.makedirs(Config.DB_PATH, exist_ok=True)

        serializable_data = self._make_serializable(self.__export_data)

        with open(file_path, "w") as file:
            json.dump(serializable_data, file, indent=2)

        logging.info(f"Data written to {file_path}")
