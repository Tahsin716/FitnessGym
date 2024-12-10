import logging
from typing import Tuple, List

from src.business_layer.exception.security_exception import SecurityException
from src.data_layer.entities.payment import Payment
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.subscription_plan import SubscriptionPlan
from src.data_layer.repository.payment_repository import PaymentRepository


class PaymentService:
    def __init__(self):
        self.payment_repository = PaymentRepository()

    def create(self, data: dict) -> Tuple[bool, str, Payment | None]:
        try:
            if not data:
                raise SecurityException("Data cannot be empty")

            required_fields = ['member_id', 'payment_method', 'subscription_plan', 'amount']
            for field in required_fields:
                if not data.get(field):
                    raise SecurityException(f"{field.replace('_', ' ')} cannot be empty")

            if not isinstance(data['payment_method'], PaymentMethod):
                raise SecurityException("Invalid payment method")

            if not isinstance(data['subscription_plan'], SubscriptionPlan):
                raise SecurityException("Invalid subscription plan")

            if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
                raise SecurityException("Amount must be a positive number")

            payment = self.payment_repository.create(data)
            return True, "", payment
        except SecurityException as e:
            logging.error(f"SecurityException occurred while creating payment: {str(e)}")
            return False, str(e), None
        except Exception as e:
            logging.error(f"Error occurred while creating payment: {str(e)}")
            return False, str(e), None

    def get_all(self) -> List[Payment]:
        return self.payment_repository.get_all()


