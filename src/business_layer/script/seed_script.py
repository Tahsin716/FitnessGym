import json
import logging
import os

from src.business_layer.providers.config import Config
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.business_layer.services.zone_service import ZoneService
from src.data_layer.enum.membership_type import MembershipType
from src.data_layer.enum.role import Role
from src.data_layer.enum.zone_type import ZoneType


class SeedScript:
    def __init__(self):
        self.__data = {}
        self.__gym_service = GymService()
        self.__staff_member_service = StaffMemberService()
        self.__zone_service = ZoneService()
        self.__gym_member_service = GymMemberService()
        self.__seed_data()

    def __seed_data(self):
        self.__read_file()
        self.__seed_gyms()
        self.__seed_staff()
        self.__seed_zones()
        self.__seed_gym_members()

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


