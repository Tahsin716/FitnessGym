from datetime import datetime


class Common:

    @staticmethod
    def calculate_duration(start_time: str, end_time: str) -> int:
        base_date = datetime.today().date()
        checkin_datetime = datetime.combine(base_date, datetime.strptime(start_time, "%H:%M").time())
        checkout_datetime = datetime.combine(base_date, datetime.strptime(end_time, "%H:%M").time())

        duration = int((checkout_datetime - checkin_datetime).total_seconds() / 60)

        return duration if duration >= 0 else 0