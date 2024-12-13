import json
import logging
import os

from src.business_layer.providers.config import Config
from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.attendance_service import AttendanceService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.payment_service import PaymentService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.business_layer.services.subscription_service import SubscriptionService
from src.business_layer.services.zone_service import ZoneService
from src.data_layer.enum.appointment_status import AppointmentStatus
from src.data_layer.enum.appointment_type import AppointmentType
from src.data_layer.enum.membership_type import MembershipType
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.role import Role
from src.data_layer.enum.subscription_plan import SubscriptionPlan
from src.data_layer.enum.zone_type import ZoneType


class SeedScript:
    def __init__(self):
        self.__data = {}
        self.__gym_service = GymService()
        self.__staff_member_service = StaffMemberService()
        self.__zone_service = ZoneService()
        self.__gym_member_service = GymMemberService()
        self.__appointment_service = AppointmentService()
        self.__subscription_service = SubscriptionService()
        self.__payment_service = PaymentService()
        self.__attendance_service = AttendanceService()
        self.__seed_data()

    def __seed_data(self):
        self.__read_file()
        self.__seed_gyms()
        self.__seed_staff()
        self.__seed_zones()
        self.__seed_gym_members()
        self.__seed_appointments()
        self.__seed_subscriptions()
        self.__seed_attendances()
        self.__seed_payments()

    def __read_file(self):
        file_path = os.path.join(Config.DB_PATH, Config.DB_NAME)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r") as file:
            self.__data = json.load(file)
            logging.info("File read")

    def __seed_gyms(self):
        gyms = self.__data.get("Gyms", [])

        for gym in gyms:
            self.__gym_service.create(gym)

        logging.info("Seeded gyms repository")

    def __seed_staff(self):
        staffs = self.__data.get("StaffMembers", [])

        for staff in staffs:
            staff['role'] = Role(staff['role'])
            self.__staff_member_service.create(staff)

        logging.info("Seeded staffs repository")

    def __seed_zones(self):
        zones = self.__data.get("Zones", [])

        for zone in zones:
            zone['zone_type'] = ZoneType(zone['zone_type'])
            self.__zone_service.create(zone)

    def __seed_gym_members(self):
        members = self.__data.get("GymMembers", [])

        for member in members:
            member['membership_type'] = MembershipType(member['membership_type'])
            self.__gym_member_service.create(member)

    def __seed_appointments(self):
        appointments = self.__data.get("Appointments", [])

        for appointment in appointments:
            appointment["appointment_type"] = AppointmentType(appointment["appointment_type"])
            appointment["status"] = AppointmentStatus(appointment["status"])
            self.__appointment_service.create(appointment)

    def __seed_subscriptions(self):
        subscriptions = self.__data.get("Subscriptions", [])

        for subscription in subscriptions:
            subscription["subscription_plan"] = SubscriptionPlan(subscription["subscription_plan"])
            subscription["payment_method"] = PaymentMethod(subscription["payment_method"])
            self.__subscription_service.create(subscription)

    def __seed_payments(self):
        payments = self.__data.get("Payments", [])

        for payment in payments:
            payment["subscription_plan"] = SubscriptionPlan(payment["subscription_plan"])
            payment["payment_method"] = PaymentMethod(payment["payment_method"])
            self.__payment_service.create(payment)

    def __seed_attendances(self):
        attendances = self.__data.get("Attendances", [])

        for attendance in attendances:
            self.__attendance_service.create(attendance)
