from typing import Dict, cast

from src.data_layer.entities.workout_zone import WorkoutZone


class ZoneRepository:
    _instance : "ZoneRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__zones = cast(Dict[str, WorkoutZone], {})
        return cls._instance

    def create(self, data: dict) -> WorkoutZone:
        zone = WorkoutZone(data)
        self.__zones[zone.id] = zone
        return zone

    def update(self, _id: str, data: dict) -> WorkoutZone:
        zone = self.__zones[_id]
        zone.gym_id = data['gym_id']
        zone.zone_type = data['zone_type']
        zone.attendant_id = data['attendant_id']
        return zone

    def get_all_gyms(self) -> list[WorkoutZone]:
        return list(self.__zones.values())

    def get_gym_by_id(self, _id: str) -> WorkoutZone:
        return self.__zones.get(_id)

    def remove(self, _id: str):
        if _id in self.__zones:
            del self.__zones[_id]