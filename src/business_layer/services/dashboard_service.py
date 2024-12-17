import datetime
from collections import Counter

from src.business_layer.services.attendance_service import AttendanceService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.payment_service import PaymentService
from src.business_layer.services.subscription_service import SubscriptionService
from src.business_layer.utils.common import Common
from src.data_layer.entities.attendance import Attendance
from src.data_layer.enum.appointment_type import AppointmentType
from src.data_layer.enum.subscription_plan import SubscriptionPlan
from src.data_layer.repository.appointment_repository import AppointmentRepository


class DashboardService:
    def __init__(self):
        self.__appointment_repository = AppointmentRepository()
        self.__subscription_service = SubscriptionService()
        self.__payment_service = PaymentService()
        self.__attendance_service = AttendanceService()
        self.__gym_service = GymService()

    def get_current_month_appointment_data(self):
        appointments = self.__appointment_repository.get_all()
        current_date = datetime.datetime.now()
        current_month_appointments = [appointment for appointment in appointments
                                      if appointment.scheduled_date.month == current_date.month and  appointment.scheduled_date.year == current_date.year]

        if not current_month_appointments:
            return {
                "Total": 0,
                "PersonalTraining" : 0,
                "GroupClass" : 0,
                "NutritionConsultant" : 0,
            }
        else:
            return {
                "Total": len(current_month_appointments),
                "PersonalTraining": len([appointment for appointment in current_month_appointments if appointment.appointment_type == AppointmentType.PERSONAL_TRAINING]),
                "GroupClass": len([appointment for appointment in current_month_appointments if appointment.appointment_type == AppointmentType.GROUP_CLASS]),
                "NutritionConsultant": len([appointment for appointment in current_month_appointments if appointment.appointment_type == AppointmentType.NUTRITION_CONSULTATION])
            }

    def get_current_month_subscription_data(self):
        subscriptions = self.__subscription_service.get_all()
        current_date = datetime.datetime.now()
        current_month_subscriptions = [subscription for subscription in subscriptions
                                       if subscription.create_date.month == current_date.month and subscription.create_date.year == current_date.year]

        if not current_month_subscriptions:
            return {
                "Total": 0,
                "Monthly": 0,
                "Quarterly": 0,
                "Annual": 0
            }
        else:
            return {
                "Total": len(current_month_subscriptions),
                "Monthly": len([subscription for subscription in current_month_subscriptions if subscription.subscription_plan == SubscriptionPlan.MONTHLY]),
                "Quarterly": len([subscription for subscription in current_month_subscriptions if subscription.subscription_plan == SubscriptionPlan.QUARTERLY]),
                "Annual": len([subscription for subscription in current_month_subscriptions if subscription.subscription_plan == SubscriptionPlan.ANNUAL])
            }

    def get_current_month_payment_data(self):
        payments = self.__payment_service.get_all()
        current_date = datetime.datetime.now()
        current_month_payments = [payment for payment in payments
                                  if payment.create_date.month == current_date.month and payment.create_date.year == current_date.year]

        if not current_month_payments:
            return {
                "Total": 0,
                "Amount": 0
            }
        else:
            return {
                "Total": len(current_month_payments),
                "Amount": sum(payment.amount for payment in current_month_payments)
            }

    def get_current_month_attendance(self):
        attendances = self.__attendance_service.get_all()
        current_date = datetime.datetime.now()
        current_month_attendances = [attendance for attendance in attendances
                                     if attendance.create_date.month == current_date.month and attendance.create_date.year == current_date.year]

        if not current_month_attendances:
            return {
                "Total": 0,
            }
        else:
            return {
                "Total": len(current_month_attendances),
                "PopularGymLocation": self.__get_popular_gym_location(current_month_attendances),
                "PeakHour": self.__get_peak_hour(current_month_attendances),
                "TotalDuration": self.__get_total_duration(current_month_attendances)
            }

    def __get_popular_gym_location(self, attendances : list[Attendance]) -> str:
        gym_ids = [attendance.gym_id for attendance in attendances]
        counter = Counter(gym_ids)

        popular_gym_id = counter.most_common(1)[0][0]
        _, _, popular_gym = self.__gym_service.get_gym_by_id(popular_gym_id)

        return popular_gym.location

    @staticmethod
    def __get_total_duration(attendances : list[Attendance]) -> str:
        return Common.convert_minutes_to_hours_and_minutes_str(sum(attendance.duration for attendance in attendances))

    @staticmethod
    def __get_peak_hour(attendances: list[Attendance]) -> str:
        hours = [int(attendance.checkin_time.split(':')[0]) for attendance in attendances]
        hour_counter = Counter(hours)

        if not hour_counter:
            return "No Peak Hour"

        peak_hour, _ = hour_counter.most_common(1)[0]

        if peak_hour == 0:
            return "12 AM"
        elif peak_hour < 12:
            return f"{peak_hour} AM"
        elif peak_hour == 12:
            return "12 PM"
        else:
            return f"{peak_hour - 12} PM"

