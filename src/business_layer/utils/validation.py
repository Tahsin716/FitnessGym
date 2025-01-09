import datetime
import re


class Validator:

    @staticmethod
    def is_valid_datetime(date : str) -> bool:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_time_format(time_str: str) -> bool:
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_phone_number(phone_number : str) -> bool:
        phone_regex = r"^\+?[0-9\s\-()]+$"
        return bool(re.match(phone_regex, phone_number))

    @staticmethod
    def validate_email(email : str) -> bool:
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_regex, email))