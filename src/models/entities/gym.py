from dataclasses import dataclass
import datetime

from src.models.entities.base_entity import BaseEntity
from src.models.utils.common import Common


@dataclass
class Gym(BaseEntity):
    def __init__(self, data: dict):
        super().__init__()
        self.__post_code: str = data['post_code']
        self.__address: str = data['address']
        self.__contact_number: str = data['contact_number']
        self.__email: str = data['email']

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
    def contact_number(self) -> str:
        return self.__contact_number

    @contact_number.setter
    def contact_number(self, value: str) -> None:
        self.__contact_number = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = value