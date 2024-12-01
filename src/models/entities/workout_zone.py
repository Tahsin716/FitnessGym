from dataclasses import dataclass

from src.models.entities.base_entity import BaseEntity
from src.models.enum.zone_type import ZoneType


@dataclass
class WorkoutZone(BaseEntity):
    def __init__(self, data : dict):
        super().__init__()
        self.__gym_id : str = data['gym_id']
        self.__zone_type : ZoneType = data['zone_type']
        self.__attendant_id : str = data['attendant_id']

    @property
    def gym_id(self) -> str:
        return self.__gym_id

    @gym_id.setter
    def gym_id(self, value: str) -> None:
        self.__gym_id = value

    @property
    def zone_type(self) -> ZoneType:
        return self.__zone_type

    @zone_type.setter
    def zone_type(self, zone_type : ZoneType) -> None:
        self.__zone_type = zone_type

    @property
    def attendant_id(self) -> str:
        return self.__attendant_id

    @attendant_id.setter
    def attendant_id(self, _id: str) -> None:
        self.__attendant_id = _id

