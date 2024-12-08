from src.data_layer.entities.member import Member
from src.data_layer.enum.role import Role


class StaffMember(Member):
    def __init__(self, data : dict):
        super().__init__(data)
        self.__role : Role = data['role']
        self.__gym_id : str = data['gym_id']

    @property
    def role(self) -> Role:
        return self.__role

    @property
    def gym_id(self) -> str:
        return self.__gym_id

    @role.setter
    def role(self, value : Role):
        self.__role = value

    @gym_id.setter
    def gym_id(self, value : str):
        self.__gym_id = value