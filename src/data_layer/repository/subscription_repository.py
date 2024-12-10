from typing import Dict, List, cast

from src.data_layer.entities.subscription import Subscription


class SubscriptionRepository:
    _instance: "SubscriptionRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__subscriptions = cast(Dict[str, Subscription], {})
        return cls._instance

    def create(self, data: dict) -> Subscription:
        subscription = Subscription(data)
        self.__subscriptions[subscription.id] = subscription
        return subscription

    def update(self, _id: str, data: dict) -> Subscription:
        subscription = self.__subscriptions[_id]
        subscription.subscription_plan = data['subscription_plan']
        subscription.payment_method = data['payment_method']
        subscription.discount = data['discount']
        subscription.loyalty_points = data['loyalty_points']
        return subscription

    def get_all(self) -> List[Subscription]:
        return list(self.__subscriptions.values())

    def get_by_id(self, _id: str) -> Subscription:
        return self.__subscriptions.get(_id)

    def delete(self, _id: str) -> None:
        if _id in self.__subscriptions:
            del self.__subscriptions[_id]

    def cancel(self, _id : str):
        subscription = self.__subscriptions[_id]
        subscription.active = False