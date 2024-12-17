from datetime import datetime

from src.business_layer.exception.security_exception import SecurityException


class Common:

    @staticmethod
    def calculate_duration(start_time: str, end_time: str) -> int:
        base_date = datetime.today().date()
        checkin_datetime = datetime.combine(base_date, datetime.strptime(start_time, "%H:%M").time())
        checkout_datetime = datetime.combine(base_date, datetime.strptime(end_time, "%H:%M").time())

        duration = int((checkout_datetime - checkin_datetime).total_seconds() / 60)

        return duration if duration >= 0 else 0

    @staticmethod
    def convert_minutes_to_hours_and_minutes_str(total_minutes):
        if total_minutes < 0:
            raise SecurityException("Invalid input: Total minutes cannot be negative.")
        elif total_minutes < 60:
            return f"{total_minutes} minutes"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours} {'hours' if hours > 1 else 'hour'} {minutes} {'minutes' if minutes > 1 else 'minute'}"
