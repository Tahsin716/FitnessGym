import logging
from typing import Tuple

from src.data_layer.entities.gym import Gym
from src.business_layer.exception.security_exception import SecurityException


class GymService:
    def __init__(self):
        self.__gyms : dict[str, Gym] = {}

    def create_gym(self, data : dict) -> Tuple[bool, str, Gym | None]:
        try:
            if data is None:
                raise SecurityException("data cannot be empty")

            if data['post_code'] is None or len(data['post_code']) == 0:
                raise Exception("post code cannot be empty")

            if data['address'] is None or len(data['address']) == 0:
                raise Exception("address cannot be empty")

            if data['contact_number'] is None or len(data['contact_number']) == 0:
                raise Exception("invalid contact number")

            if data['email'] is None or len(data['email']) == 0:
                raise Exception("invalid email")

            gym = Gym({})
            self.__gyms[gym.id] = gym

            return True, "", gym
        except SecurityException as e:
            logging.error(f"SecurityException occurred while saving gym: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while saving gym: {str(e)}")
            return False, str(e), None

    def update_gym(self, _id : str, data : dict) -> Tuple[bool, str, Gym | None]:
        try:
            if data is None:
                raise SecurityException("data cannot be empty")

            if data['post_code'] is None or len(data['post_code']) == 0:
                raise Exception("post code cannot be empty")

            if data['address'] is None or len(data['address']) == 0:
                raise Exception("address cannot be empty")

            if data['contact_number'] is None or len(data['contact_number']) == 0:
                raise Exception("invalid contact number")

            if data['email'] is None or len(data['email']) == 0:
                raise Exception("invalid email")

            gym = self.__gyms[_id]

            if gym is None:
                raise SecurityException("no gym exists with given id")

            gym.post_code = data['post_code']
            gym.address = data['address']
            gym.contact_number = data['contact_number']
            gym.email = data['email']

            return True, "", gym
        except SecurityException as e:
            logging.error(f"SecurityException occurred while updating gym: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while updating gym: {str(e)}")
            return False, str(e), None

    def get_all_gyms(self) -> list[Gym]:
        return list(self.__gyms.values())

    def get_gym_by_id(self, _id : str) -> Tuple[bool, str, Gym | None]:
        try:
            gym = self.__gyms[_id]

            if gym is None:
                raise SecurityException("no gym exists with given id")

            return True, "", gym
        except SecurityException as e:
            logging.error(f"SecurityException occurred while retrieving gym: {str(e)}")
            return False, str(e), None

    def remove_gym(self, _id : str):
        del self.__gyms[_id]

