import logging
from typing import Tuple, List

from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.entities.subscription import Subscription
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.subscription_plan import SubscriptionPlan
from src.data_layer.repository.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(self):
        self.subscription_repository = SubscriptionRepository()

    def create(self, data: dict) -> Tuple[bool, str, Subscription | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['member_id', 'subscription_plan', 'payment_method', 'discount', 'loyalty_points']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['subscription_plan'], SubscriptionPlan):
                raise SecurityException("Invalid subscription plan")

            if not isinstance(data['payment_method'], PaymentMethod):
                raise SecurityException("Invalid payment method")

            if not isinstance(data['discount'], (int, float)) or data['discount'] < 0:
                raise SecurityException("Discount must be a non-negative number")

            if not isinstance(data['loyalty_points'], (int, float)) or data['loyalty_points'] < 0:
                raise SecurityException("Loyalty points must be a non-negative number")

            subscription = self.subscription_repository.create(data)
            return True, "", subscription
        except SecurityException as e:
            logging.error(f"SecurityException occurred while creating subscription: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while creating subscription: {str(e)}")
            return False, str(e), None

    def update(self, _id: str, data: dict) -> Tuple[bool, str, Subscription | None]:
        try:
            subscription = self.subscription_repository.get_by_id(_id)
            if not subscription:
                raise SecurityException("No subscription exists with the given ID")

            required_fields = ['subscription_plan', 'payment_method', 'discount', 'loyalty_points']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['subscription_plan'], SubscriptionPlan):
                raise SecurityException("Invalid subscription plan")

            if not isinstance(data['payment_method'], PaymentMethod):
                raise SecurityException("Invalid payment method")

            if not isinstance(data['discount'], (int, float)) or data['discount'] < 0:
                raise SecurityException("Discount must be a non-negative number")

            if not isinstance(data['loyalty_points'], (int, float)) or data['loyalty_points'] < 0:
                raise SecurityException("Loyalty points must be a non-negative number")

            subscription = self.subscription_repository.update(_id, data)
            return True, "", subscription
        except SecurityException as e:
            logging.error(f"SecurityException occurred while updating subscription: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while updating subscription: {str(e)}")
            return False, str(e), None

    def get_all(self) -> List[Subscription]:
        return self.subscription_repository.get_all()

    def get_by_id(self, _id: str) -> Tuple[bool, str, Subscription | None]:
        try:
            subscription = self.subscription_repository.get_by_id(_id)
            if not subscription:
                raise SecurityException("No subscription exists with the given ID")
            return True, "", subscription
        except SecurityException as e:
            logging.error(f"SecurityException occurred while retrieving subscription: {str(e)}")
            return False, str(e), None

    def cancel(self, _id: str) -> Tuple[bool, str]:
        try:
            subscription = self.subscription_repository.get_by_id(_id)
            if not subscription:
                raise SecurityException("No subscription exists with the given ID")

            self.subscription_repository.cancel(_id)
            return True, "Subscription canceled successfully"
        except SecurityException as e:
            logging.error(f"SecurityException occurred while canceling subscription: {str(e)}")
            return False, str(e)
        except Exception as e:
            logging.error(f"Error occurred while canceling subscription: {str(e)}")
            return False, str(e)
