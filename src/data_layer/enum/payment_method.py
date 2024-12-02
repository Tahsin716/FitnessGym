from enum import Enum


class PaymentMethod(Enum):
    CREDIT_CARD = "credit card"
    DEBIT_CARD = "debit card"
    BANK_TRANSFER = "bank transfer"
    CASH = "cash"