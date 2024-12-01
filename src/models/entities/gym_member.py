from dataclasses import dataclass
import datetime

from src.models.entities.member import Member
from src.models.enum.membership_type import MembershipType


@dataclass
class GymMember(Member):
    def __init__(self, data : dict):
        super().__init__(data)
        self.__membership_type : MembershipType = data['membership_type']
        self.__membership_start_date : datetime = datetime.datetime.now(datetime.timezone.utc)
        self.__height : float = data['height']
        self.__weight : float = data['weight']

