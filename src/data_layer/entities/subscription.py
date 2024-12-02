
from src.data_layer.entities.base_entity import BaseEntity
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.subscription_plan import SubscriptionPlan


class Subscription(BaseEntity):
    def __init__(self, data : dict):
        super().__init__()
        self.__member_id : str = data['member_id']
        self.__subscription_plan : SubscriptionPlan = data['subscription_type']
        self.__monthly_rate : float = self.__get_monthly_rate()
        self.__payment_method : PaymentMethod = data['payment_method']
        self.__discount : float = data['discount']
        self.__active : bool = True
        self.__loyalty_points : int = 0

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def subscription_plan(self) -> SubscriptionPlan:
        return self.__subscription_plan

    @property
    def monthly_rate(self) -> float:
        return self.__monthly_rate

    @property
    def payment_method(self) -> PaymentMethod:
        return self.__payment_method

    @property
    def discount(self) -> float:
        return self.__discount

    @property
    def loyalty_points(self) -> int:
        return self.__loyalty_points

    @property
    def active(self) -> bool:
        return self.__active

    @subscription_plan.setter
    def subscription_plan(self, value: SubscriptionPlan):
        self.__subscription_plan = value
        self.__monthly_rate = self.__get_monthly_rate()

    @payment_method.setter
    def payment_method(self, value: PaymentMethod):
        self.__payment_method = value

    @discount.setter
    def discount(self, value: float):
        self.__discount = value

    @loyalty_points.setter
    def loyalty_points(self, value: int):
        self.__loyalty_points = value

    @active.setter
    def active(self, value : bool):
        self.__active = value

    def __get_monthly_rate(self) -> float:
        if self.__subscription_plan == SubscriptionPlan.MONTHLY:
            return 14.0
        elif self.__subscription_plan == SubscriptionPlan.QUARTERLY:
            return 12.0
        else:
            return 10.0

