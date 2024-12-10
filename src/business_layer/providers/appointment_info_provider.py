from src.data_layer.enum.appointment_type import AppointmentType


class AppointmentProvider:
    APPOINTMENT_DURATION : list[str] = ["30", "60", "90"]

    APPOINTMENT_COST_PER_SESSION : dict[str, float] = {
        AppointmentType.PERSONAL_TRAINING.value : 25.0,
        AppointmentType.GROUP_CLASS.value : 35.0,
        AppointmentType.NUTRITION_CONSULTATION.value : 40.0
    }