import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.appointment_service import AppointmentService
from src.data_layer.enum.appointment_type import AppointmentType
from src.data_layer.enum.role import Role


class UpdateAppointmentForm(tk.Toplevel):
    def __init__(self, parent, gym_service: GymService,
                 staff_member_service: StaffMemberService,
                 gym_member_service: GymMemberService,
                 appointment_service: AppointmentService,
                 appointment_data: dict,
                 callback):
        super().__init__(parent)
        self.gym_service = gym_service
        self.staff_member_service = staff_member_service
        self.gym_member_service = gym_member_service
        self.appointment_service = appointment_service
        self.appointment_data = appointment_data
        self.callback = callback

        self.title("Update Appointment")
        self.geometry("500x500")

        # Variables to store form data
        self.gym_location = tk.StringVar(value=appointment_data['gym'])
        self.gym_member = tk.StringVar(value=appointment_data['member'])
        self.staff_member = tk.StringVar(value=appointment_data['staff'])
        self.appointment_type = tk.StringVar(value=appointment_data['appointment_type'])
        self.schedule_date = tk.StringVar(value=appointment_data['scheduled_date'])
        self.duration = tk.StringVar(value=str(appointment_data['duration']))
        self.appointment_id = appointment_data['id']

        # Populate gym locations
        gyms = self.gym_service.get_all_gyms()
        self.gym_locations = [gym.location for gym in gyms]
        self.gym_ids = {gym.location: gym.id for gym in gyms}

        # Gym Location Dropdown
        ttk.Label(self, text="Gym Location").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.gym_location_dropdown = ttk.Combobox(
            self,
            textvariable=self.gym_location,
            values=self.gym_locations,
            state="readonly"
        )
        self.gym_location_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.gym_location_dropdown.bind('<<ComboboxSelected>>', self.on_gym_location_selected)

        # Member Dropdown
        ttk.Label(self, text="Member").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        gym_members = self.gym_member_service.get_all()
        self.gym_member_names = [f"{member.first_name} {member.last_name}" for member in gym_members]
        self.gym_member_ids = {f"{member.first_name} {member.last_name}": member.id for member in gym_members}

        self.gym_member_dropdown = ttk.Combobox(
            self,
            textvariable=self.gym_member,
            values=self.gym_member_names,
            state="readonly"
        )
        self.gym_member_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Appointment Type Dropdown
        ttk.Label(self, text="Appointment Type").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.appointment_type_dropdown = ttk.Combobox(
            self,
            textvariable=self.appointment_type,
            values=[at.value for at in AppointmentType],
            state="readonly"
        )
        self.appointment_type_dropdown.grid(row=2, column=1, padx=10, pady=5)
        self.appointment_type_dropdown.bind('<<ComboboxSelected>>', self.on_appointment_type_selected)

        # Staff Dropdown (dynamically populated)
        ttk.Label(self, text="Staff").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.staff_dropdown = ttk.Combobox(
            self,
            textvariable=self.staff_member,
            state="readonly"
        )
        self.staff_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Schedule Date
        ttk.Label(self, text="Schedule Date").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.schedule_date_entry = ttk.Entry(self, textvariable=self.schedule_date)
        self.schedule_date_entry.grid(row=4, column=1, padx=10, pady=5)

        # Duration
        ttk.Label(self, text="Duration (minutes)").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(
            self,
            textvariable=self.duration
        )
        self.duration_entry.grid(row=5, column=1, padx=10, pady=5)

        # Buttons
        ttk.Button(self, text="Update", command=self.update_appointment).grid(row=6, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=6, column=1, padx=10, pady=10)

        self.staff_member_ids = {}


    def on_gym_location_selected(self, event=None):
        # Clear previous staff selection
        self.staff_member.set('')
        staff_members = []

        # Get the selected gym's ID
        selected_gym_location = self.gym_location.get()
        selected_gym_id = self.gym_ids[selected_gym_location]

        appointment_type = self.appointment_type.get()

        if appointment_type:
            if appointment_type == AppointmentType.GROUP_CLASS.value or appointment_type == AppointmentType.PERSONAL_TRAINING.value:
                role = Role.TRAINER
            else:
                role = Role.NUTRITIONIST

            staff_members = self.staff_member_service.get_all_by_role_and_gym(role, selected_gym_id)

        # Populate staff dropdown
        if staff_members:
            staff_names = [f"{staff.first_name} {staff.last_name}" for staff in staff_members]
            self.staff_member_ids = {f"{staff.first_name} {staff.last_name}": staff.id for staff in staff_members}

            self.staff_dropdown['values'] = staff_names
            self.staff_dropdown['state'] = 'readonly'
        else:
            self.staff_dropdown['values'] = []
            self.staff_dropdown['state'] = 'disabled'

    def on_appointment_type_selected(self, event=None):
        # This will trigger staff dropdown population based on gym and appointment type
        self.on_gym_location_selected()

    def update_appointment(self):
        data = {
            "member_id": self.gym_member_ids.get(self.gym_member.get(), None),
            "gym_id": self.gym_ids.get(self.gym_location.get(), None),
            "staff_id": self.staff_member_ids.get(self.staff_member.get(), None),
            "appointment_type": AppointmentType(self.appointment_type.get()) if self.appointment_type.get() else None,
            "schedule_date": self.schedule_date_entry.get(),
            "duration": self.duration.get()
        }

        success, message, appointment = self.appointment_service.update(self.appointment_id, data)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Appointment updated successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()