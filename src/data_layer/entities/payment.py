from src.data_layer.entities.base_entity import BaseEntity
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.subscription_plan import SubscriptionPlan


class Payment(BaseEntity):
    def __init__(self, data : dict):
        super().__init__()
        self.__member_id : str = data['member_id']
        self.__payment_method : PaymentMethod = data['payment_method']
        self.__subscription_plan : SubscriptionPlan = data['subscription_plan']
        self.__amount : float = data['amount']