from typing import Dict, List, cast

from src.data_layer.entities.staff_member import StaffMember


class StaffMemberRepository:
    _instance: "StaffMemberRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__staff_members = cast(Dict[str, StaffMember], {})
        return cls._instance

    def create(self, data: dict) -> StaffMember:
        staff_member = StaffMember(data)
        self.__staff_members[staff_member.id] = staff_member
        return staff_member

    def update(self, _id: str, data: dict) -> StaffMember:
        staff_member = self.__staff_members[_id]
        staff_member.first_name = data['first_name']
        staff_member.last_name = data['last_name']
        staff_member.email = data['email']
        staff_member.phone_number = data['phone_number']
        staff_member.role = data['role']
        staff_member.gym_id = data['gym_id']
        return staff_member

    def get_all(self) -> List[StaffMember]:
        return list(self.__staff_members.values())

    def get_by_id(self, _id: str) -> StaffMember:
        return self.__staff_members.get(_id)

    def delete(self, _id: str) -> None:
        if _id in self.__staff_members:
            del self.__staff_members[_id]
