import datetime

from src.models.entities.member import Member
from src.models.enum.membership_type import MembershipType


class GymMember(Member):
    def __init__(self, data : dict):
        super().__init__(data)
        self.__membership_type : MembershipType = data['membership_type']
        self.__membership_start_date : datetime = datetime.datetime.now(datetime.timezone.utc)
        self.__height : float = data['height']
        self.__weight : float = data['weight']

    @property
    def membership_type(self) -> MembershipType:
        return self.__membership_type

    @membership_type.setter
    def membership_type(self, value: MembershipType):
        self.__membership_type = value

    @property
    def membership_start_date(self) -> datetime:
        return self.__membership_start_date

    @property
    def height(self) -> float:
        return self.__height

    @height.setter
    def height(self, value: float):
        self.__height = value

    @property
    def weight(self) -> float:
        return self.__height

    @weight.setter
    def weight(self, value: float):
        self.__weight = value