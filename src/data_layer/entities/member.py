from src.data_layer.entities.base_entity import BaseEntity


class Member(BaseEntity):
    def __init__(self, data : dict):
        super().__init__(data['_id'], data['create_date'])
        self.__first_name : str = data['first_name']
        self.__last_name : str = data['last_name']
        self.__email : str = data['email']
        self.__phone_number : str = data['phone_number']

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        self.__first_name = value

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        self.__last_name = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self.__email = value

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        self.__phone_number = value

