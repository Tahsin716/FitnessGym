from dataclasses import dataclass

from src.models.entities.base_entity import BaseEntity


@dataclass
class Member(BaseEntity):
    def __init__(self, data : dict):
        super().__init__()
        self.__first_name : str = data['first_name']
        self.__last_name : str = data['last_name']
        self.__email : str = data['email']
        self.__phone_number : str = data['phone_number']

