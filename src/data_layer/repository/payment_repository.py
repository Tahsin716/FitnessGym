from typing import Dict, List, cast

from src.data_layer.entities.payment import Payment


class PaymentRepository:
    _instance: "PaymentRepository" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__payments = cast(Dict[str, Payment], {})
        return cls._instance

    def create(self, data: dict) -> Payment:
        payment = Payment(data)
        self.__payments[payment.id] = payment
        return payment

    def get_all(self) -> List[Payment]:
        return list(self.__payments.values())
