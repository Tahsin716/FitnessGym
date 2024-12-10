import logging
from typing import Tuple, List

from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.entities.gym_member import GymMember
from src.data_layer.enum.membership_type import MembershipType
from src.data_layer.repository.gym_member_repository import GymMemberRepository
from src.data_layer.repository.subscription_repository import SubscriptionRepository


class GymMemberService:
    def __init__(self):
        self.gym_member_repository = GymMemberRepository()
        self.subscription_repository = SubscriptionRepository()

    def create(self, data: dict) -> Tuple[bool, str, GymMember | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'membership_type', 'height', 'weight']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            try:
                data['height'] = float(data['height'])
                data['weight'] = float(data['weight'])
            except ValueError:
                raise SecurityException("Invalid Height/Weight value")

            if any(x < 0 for x in [data['height'],data['weight']]):
                raise SecurityException("Height and Weight cannot be negative")

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

    def get_gym_members_with_no_active_subscriptions(self) -> list[GymMember]:
        subscriptions = self.subscription_repository.get_all()
        members = self.gym_member_repository.get_all()

        member_list = []
        member_ids_with_subscriptions = {subscription.member_id for subscription in subscriptions if subscription.active}

        for member in members:
            if not member.id in member_ids_with_subscriptions:
                member_list.append(member)

        return member_list

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
