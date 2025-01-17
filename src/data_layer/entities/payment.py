from src.data_layer.entities.base_entity import BaseEntity
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.subscription_plan import SubscriptionPlan


class Payment(BaseEntity):
    def __init__(self, data : dict):
        _id = data.get('_id', None)
        create_date = data.get('create_date', None)
        super().__init__(_id, create_date)

        self.__member_id : str = data['member_id']
        self.__payment_method : PaymentMethod = data['payment_method']
        self.__subscription_plan : SubscriptionPlan = data['subscription_plan']
        self.__appointment_ids : list[str] = data.get('appointment_ids', [])
        self.__amount : float = data['amount']

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def payment_method(self) -> PaymentMethod:
        return self.__payment_method

    @property
    def subscription_plan(self) -> SubscriptionPlan:
        return self.__subscription_plan

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def appointment_ids(self)  -> list[str]:
        return self.__appointment_ids