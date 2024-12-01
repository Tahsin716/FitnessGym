import logging
from typing import Tuple

from src.models.entities.gym import Gym
from src.models.exception.security_exception import SecurityException


class GymRepository:
    def __init__(self):
        self.__gyms : list[Gym] = []

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
            self.__gyms.append(gym)

            return True, "", gym
        except SecurityException as e:
            logging.error(f"SecurityException occurred while saving gym: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while saving gym: {str(e)}")
            return False, str(e), None

