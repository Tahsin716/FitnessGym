
from src.data_layer.entities.base_entity import BaseEntity


class Subscription(BaseEntity):
    def __init__(self, data : dict):
        super().__init__()
        self.__member_id : str = data['member_id']
        self.__subscription_type = data['subscription_type']
        self.__monthly_rate : float = data['monthly_rate']
        self.__payment_method = data['payment_method']
        self.__discount : float = data['discount']
        self.__loyalty_points : int = 0

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def subscription_type(self) -> str:
        return self.__subscription_type

    @property
    def monthly_rate(self) -> float:
        return self.__monthly_rate

    @property
    def payment_method(self) -> str:
        return self.__payment_method

    @property
    def discount(self) -> float:
        return self.__discount

    @property
    def loyalty_points(self) -> int:
        return self.__loyalty_points

    @subscription_type.setter
    def subscription_type(self, value: str):
        self.__subscription_type = value

    @monthly_rate.setter
    def monthly_rate(self, value: float):
        self.__monthly_rate = value

    @payment_method.setter
    def payment_method(self, value: str):
        self.__payment_method = value

    @discount.setter
    def discount(self, value: float):
        self.__discount = value

    @loyalty_points.setter
    def loyalty_points(self, value: int):
        self.__loyalty_points = value

