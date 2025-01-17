from src.data_layer.entities.base_entity import BaseEntity
from src.data_layer.enum.zone_type import ZoneType


class Zone(BaseEntity):
    def __init__(self, data : dict):
        _id = data.get('_id', None)
        create_date = data.get('create_date', None)
        super().__init__(_id, create_date)

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

