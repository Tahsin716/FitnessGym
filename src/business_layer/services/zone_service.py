import logging
from typing import Tuple

from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.entities.zone import Zone
from src.data_layer.enum.zone_type import ZoneType
from src.data_layer.repository.zone_repository import ZoneRepository


class ZoneService:
    def __init__(self):
        self.zone_repository = ZoneRepository()

    def create(self, data: dict) -> Tuple[bool, str, Zone | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['gym_id', 'zone_type', 'attendant_id']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['zone_type'], ZoneType):
                raise SecurityException("Invalid zone type")

            zone = self.zone_repository.create(data)

            return True, "", zone
        except SecurityException as e:
            logging.error(f"SecurityException occurred while saving zone: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while saving zone: {str(e)}")
            return False, str(e), None

    def update(self, _id: str, data: dict) -> Tuple[bool, str, Zone | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['gym_id', 'zone_type', 'attendant_id']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['zone_type'], ZoneType):
                raise SecurityException("Invalid zone type")

            if self.zone_repository.get_zone_by_id(_id) is None:
                raise SecurityException("No zone exists with the given ID")

            zone = self.zone_repository.update(_id, data)

            return True, "", zone
        except SecurityException as e:
            logging.error(f"SecurityException occurred while updating zone: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while updating zone: {str(e)}")
            return False, str(e), None

    def get_all_zones(self) -> list[Zone]:
        return self.zone_repository.get_all_zones()

    def get_zone_by_id(self, _id: str) -> Tuple[bool, str, Zone | None]:
        try:
            zone = self.zone_repository.get_zone_by_id(_id)

            if zone is None:
                raise SecurityException("No zone exists with the given ID")

            return True, "", zone
        except SecurityException as e:
            logging.error(f"SecurityException occurred while retrieving zone: {str(e)}")
            return False, str(e), None

    def get_zones_by_gym_id(self, gym_id : str) -> list[Zone]:
        zones = self.get_all_zones()
        return [zone for zone in zones if zone.gym_id == gym_id]

    def delete(self, _id: str) -> Tuple[bool, str]:
        try:
            if self.zone_repository.get_zone_by_id(_id) is None:
                raise SecurityException("No zone exists with the given ID")

            self.zone_repository.remove(_id)
            return True, ""
        except SecurityException as e:
            logging.error(f"SecurityException occurred while deleting zone: {str(e)}")
            return False, str(e)
        except Exception as e:
            logging.error(f"Error occurred while deleting zone: {str(e)}")
            return False, str(e)
