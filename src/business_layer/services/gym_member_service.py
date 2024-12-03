import logging
from typing import Tuple, List

from src.data_layer.entities.gym_member import GymMember
from src.data_layer.enum.membership_type import MembershipType
from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.repository.gym_member_repository import GymMemberRepository


class GymMemberService:
    def __init__(self):
        self.gym_member_repository = GymMemberRepository()

    def create(self, data: dict) -> Tuple[bool, str, GymMember | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'membership_type', 'height', 'weight']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['membership_type'], MembershipType):
                raise SecurityException("Invalid membership type")

            member = self.gym_member_repository.create(data)
            return True, "", member
        except SecurityException as e:
            logging.error(f"SecurityException occurred while creating gym member: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while creating gym member: {str(e)}")
            return False, str(e), None

    def update(self, _id: str, data: dict) -> Tuple[bool, str, GymMember | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'membership_type', 'height', 'weight']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['membership_type'], MembershipType):
                raise SecurityException("Invalid membership type")

            if self.gym_member_repository.get_by_id(_id) is None:
                raise SecurityException("No member exists with the given ID")

            member = self.gym_member_repository.update(_id, data)
            return True, "", member
        except SecurityException as e:
            logging.error(f"SecurityException occurred while updating gym member: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while updating gym member: {str(e)}")
            return False, str(e), None

    def get_all(self) -> List[GymMember]:
        return self.gym_member_repository.get_all()

    def get_by_id(self, _id: str) -> Tuple[bool, str, GymMember | None]:
        try:
            member = self.gym_member_repository.get_by_id(_id)

            if member is None:
                raise SecurityException("No member exists with the given ID")

            return True, "", member
        except SecurityException as e:
            logging.error(f"SecurityException occurred while retrieving gym member: {str(e)}")
            return False, str(e), None

    def delete(self, _id: str) -> Tuple[bool, str]:
        try:
            if self.gym_member_repository.get_by_id(_id) is None:
                raise SecurityException("No member exists with the given ID")

            self.gym_member_repository.delete(_id)
            return True, ""
        except SecurityException as e:
            logging.error(f"SecurityException occurred while deleting gym member: {str(e)}")
            return False, str(e)
        except Exception as e:
            logging.error(f"Error occurred while deleting gym member: {str(e)}")
            return False, str(e)
