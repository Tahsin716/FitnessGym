from src.models.entities.member import Member
from src.models.enum.role import Role


class StaffMember(Member):
    def __init__(self, data : dict):
        super().__init__(data)
        self.__role : Role = data['role']

    @property
    def role(self) -> Role:
        return self.__role