from dataclasses import dataclass

from src.data_layer.entities.base_entity import BaseEntity


@dataclass
class Gym(BaseEntity):
    def __init__(self, data: dict):
        _id = data.get('_id', None)
        create_date = data.get('create_date', None)
        super().__init__(_id, create_date)

        self.__location : str = data['location']
        self.__post_code: str = data['post_code']
        self.__address: str = data['address']
        self.__phone_number: str = data['phone_number']
        self.__email: str = data['email']

    @property
    def location(self) -> str:
        return self.__location

    @location.setter
    def location(self, value: str) -> None:
        self.__location = value

    @property
    def post_code(self) -> str:
        return self.__post_code

    @post_code.setter
    def post_code(self, value: str) -> None:
        self.__post_code = value

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        self.__address = value

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        self.__phone_number = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = value