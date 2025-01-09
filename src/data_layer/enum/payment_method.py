from enum import Enum


class PaymentMethod(Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    BANK_TRANSFER = "Bank Transfer"
    CASH = "Cash"