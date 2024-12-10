import logging
from typing import Tuple

from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.entities.staff_member import StaffMember
from src.data_layer.enum.role import Role
from src.data_layer.repository.staff_member_repository import StaffMemberRepository


class StaffMemberService:
    def __init__(self):
        self.staff_member_repository = StaffMemberRepository()

    def create(self, data: dict) -> Tuple[bool, str, StaffMember | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'gym_id']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['role'], Role):
                raise SecurityException("Invalid role")

            staff_member = self.staff_member_repository.create(data)
            return True, "", staff_member
        except SecurityException as e:
            logging.error(f"SecurityException occurred while creating staff member: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while creating staff member: {str(e)}")
            return False, str(e), None

    def update(self, _id: str, data: dict) -> Tuple[bool, str, StaffMember | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'gym_id']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if self.staff_member_repository.get_by_id(_id) is None:
                raise SecurityException("No staff member exists with the given ID")

            staff_member = self.staff_member_repository.update(_id, data)
            return True, "", staff_member
        except SecurityException as e:
            logging.error(f"SecurityException occurred while updating staff member: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while updating staff member: {str(e)}")
            return False, str(e), None

    def get_all(self) -> list[StaffMember]:
        return self.staff_member_repository.get_all()

    def get_all_by_role(self, role : Role ) -> list[StaffMember]:
        staffs = self.get_all()
        return [staff for staff in staffs if staff.role == role]

    def get_all_by_role_and_gym(self, role : Role, gym_id : str) -> list[StaffMember]:
        staffs = self.get_all()
        return [staff for staff in staffs if staff.role == role and staff.gym_id == gym_id]

    def get_by_id(self, _id: str) -> Tuple[bool, str, StaffMember | None]:
        try:
            staff_member = self.staff_member_repository.get_by_id(_id)

            if staff_member is None:
                raise SecurityException("No staff member exists with the given ID")

            return True, "", staff_member
        except SecurityException as e:
            logging.error(f"SecurityException occurred while retrieving staff member: {str(e)}")
            return False, str(e), None

    def delete(self, _id: str) -> Tuple[bool, str]:
        try:
            if self.staff_member_repository.get_by_id(_id) is None:
                raise SecurityException("No staff member exists with the given ID")

            self.staff_member_repository.delete(_id)
            return True, ""
        except SecurityException as e:
            logging.error(f"SecurityException occurred while deleting staff member: {str(e)}")
            return False, str(e)
        except Exception as e:
            logging.error(f"Error occurred while deleting staff member: {str(e)}")
            return False, str(e)
