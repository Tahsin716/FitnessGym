from typing import Dict, cast

from src.data_layer.entities.zone import Zone


class ZoneRepository:
    _instance : "ZoneRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__zones = cast(Dict[str, Zone], {})
        return cls._instance

    def create(self, data: dict) -> Zone:
        zone = Zone(data)
        self.__zones[zone.id] = zone
        return zone

    def update(self, _id: str, data: dict) -> Zone:
        zone = self.__zones[_id]
        zone.gym_id = data['gym_id']
        zone.zone_type = data['zone_type']
        zone.attendant_id = data['attendant_id']
        return zone

    def get_all_zones(self) -> list[Zone]:
        return list(self.__zones.values())

    def get_zone_by_id(self, _id: str) -> Zone:
        return self.__zones.get(_id)

    def remove(self, _id: str):
        if _id in self.__zones:
            del self.__zones[_id]