import datetime

from src.data_layer.entities.member import Member
from src.data_layer.enum.membership_type import MembershipType


class GymMember(Member):
    def __init__(self, data : dict):
        super().__init__(data)
        self.__membership_type : MembershipType = data['membership_type']
        self.__height : float = data['height']
        self.__weight : float = data['weight']

    @property
    def membership_type(self) -> MembershipType:
        return self.__membership_type

    @membership_type.setter
    def membership_type(self, value : MembershipType):
        self.__membership_type = value

    @property
    def height(self) -> float:
        return self.__height

    @height.setter
    def height(self, value: float):
        self.__height = value

    @property
    def weight(self) -> float:
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value
