from typing import Dict, List, cast

from src.data_layer.entities.gym_member import GymMember


class GymMemberRepository:
    _instance: "GymMemberRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__members = cast(Dict[str, GymMember], {})
        return cls._instance

    def create(self, data: dict) -> GymMember:
        member = GymMember(data)
        self.__members[member.id] = member
        return member

    def update(self, _id: str, data: dict) -> GymMember:
        member = self.__members[_id]
        member.first_name = data["first_name"]
        member.last_name = data["last_name"]
        member.email = data["email"]
        member.phone_number = data["phone_number"]
        member.membership_type = data["membership_type"]
        member.height = data["height"]
        member.weight = data["weight"]
        return member

    def get_all(self) -> List[GymMember]:
        return list(self.__members.values())

    def get_by_id(self, _id: str) -> GymMember:
        return self.__members.get(_id)

    def delete(self, _id: str) -> None:
        if _id in self.__members:
            del self.__members[_id]
