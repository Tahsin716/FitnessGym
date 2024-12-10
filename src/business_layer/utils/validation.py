import datetime

class Validator:

    @staticmethod
    def is_valid_datetime(date : str) -> bool:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False