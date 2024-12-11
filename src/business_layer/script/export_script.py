import json
import logging
import os

from src.business_layer.providers.config import Config
from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.business_layer.services.zone_service import ZoneService
from src.business_layer.services.gym_member_service import GymMemberService


class ExportScript:
    def __init__(self):
        self.__gym_service = GymService()
        self.__staff_member_service = StaffMemberService()
        self.__zone_service = ZoneService()
        self.__gym_member_service = GymMemberService()
        self.__appointment_service = AppointmentService()
        self.__export_data = {}

    def export(self):
        try:
            self.__export_gyms()
            self.__export_staff()
            self.__export_zones()
            self.__export_gym_members()
            self.__write_to_file()
            logging.info("Successfully exported all data")
        except Exception as e:
            logging.error(f"Export failed: {str(e)}")
            raise

    def __export_gyms(self):
        gyms = self.__gym_service.get_all_gyms()
        self.__export_data["Gyms"] = []

        for gym in gyms:
            data = {
                "_id": gym.id,
                "create_id": gym.create_date,
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
                "create_data": staff.create_date,
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
                "appointment_type": appointment.appointment_type.value,
                "schedule_date": appointment.scheduled_date,
                "status": appointment.status,
                "duration": appointment.duration,
                "is_paid": appointment.is_paid
            }
            self.__export_data["Appointments"].append(data)

    def __write_to_file(self):

        file_path = os.path.join(Config.DB_PATH, Config.DB_NAME)

        # Ensure the directory exists
        os.makedirs(Config.DB_PATH, exist_ok=True)

        with open(file_path, "w") as file:
            json.dump(self.__export_data, file, indent=2)

        logging.info(f"Data written to {file_path}")
