import logging
from typing import Tuple

from src.data_layer.entities.gym import Gym
from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.repository.gym_repository import GymRepository


class GymService:
    def __init__(self):
        self.gym_repository = GymRepository()

    def create(self, data : dict) -> Tuple[bool, str, Gym | None]:
        try:
            if not data:
                raise SecurityException("data cannot be empty")

            required_fields = ['post_code', 'address', 'contact_number', 'email']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            gym = self.gym_repository.create(data)

            return True, "", gym
        except SecurityException as e:
            logging.error(f"SecurityException occurred while saving gym: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while saving gym: {str(e)}")
            return False, str(e), None

    def update(self, _id : str, data : dict) -> Tuple[bool, str, Gym | None]:
        try:
            if not data:
                raise SecurityException("data cannot be empty")

            required_fields = ['post_code', 'address', 'contact_number', 'email']
            for field in required_fields:
                if not data.get(field):
                    raise Exception(f"{field.replace('_', ' ')} cannot be empty")

            if self.gym_repository.get_gym_by_id(_id) is None:
                raise SecurityException("no gym exists with given id")

            gym = self.gym_repository.update(_id, data)

            return True, "", gym
        except SecurityException as e:
            logging.error(f"SecurityException occurred while updating gym: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while updating gym: {str(e)}")
            return False, str(e), None

    def get_all_gyms(self) -> list[Gym]:
        return self.gym_repository.get_all_gyms()

    def get_gym_by_id(self, _id : str) -> Tuple[bool, str, Gym | None]:
        try:
            gym = self.gym_repository.get_gym_by_id(_id)

            if gym is None:
                raise SecurityException("no gym exists with given id")

            return True, "", gym
        except SecurityException as e:
            logging.error(f"SecurityException occurred while retrieving gym: {str(e)}")
            return False, str(e), None

    def delete(self, _id : str):
        self.gym_repository.delete(_id)

