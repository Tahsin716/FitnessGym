import datetime

from src.business_layer.services.attendance_service import AttendanceService
from src.business_layer.services.payment_service import PaymentService
from src.business_layer.services.subscription_service import SubscriptionService
from src.data_layer.enum.appointment_type import AppointmentType
from src.data_layer.repository.appointment_repository import AppointmentRepository


class DashboardService:
    def __init__(self):
        self.__appointment_repository = AppointmentRepository()
        self.__subscription_service = SubscriptionService()
        self.__payment_service = PaymentService()
        self.__attendance_service = AttendanceService()

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

