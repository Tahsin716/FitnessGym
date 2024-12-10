import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.data_layer.enum.appointment_type import AppointmentType
from src.data_layer.enum.role import Role


class CreateAppointmentForm(tk.Toplevel):
    def __init__(self, parent, gym_service: GymService,
                 staff_member_service: StaffMemberService,
                 gym_member_service: GymMemberService,
                 appointment_service: AppointmentService,
                 callback):
        super().__init__(parent)
        self.gym_service = gym_service
        self.staff_member_service = staff_member_service
        self.gym_member_service = gym_member_service
        self.appointment_service = appointment_service
        self.callback = callback

        self.title("Create Appointment")
        self.geometry("500x500")

        # Variables to store form data
        self.gym_location = tk.StringVar()
        self.gym_member = tk.StringVar()
        self.staff_member = tk.StringVar()
        self.appointment_type = tk.StringVar()
        self.schedule_date = tk.StringVar()
        self.duration = tk.StringVar()

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

        # Staff Dropdown (will be dynamically populated)
        ttk.Label(self, text="Staff").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.staff_dropdown = ttk.Combobox(
            self,
            textvariable=self.staff_member,
            state="disabled"
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
        ttk.Button(self, text="Save", command=self.save_appointment).grid(row=6, column=0, padx=10, pady=10)
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

    def save_appointment(self):

        data = {
            "member_id": self.gym_member_ids[self.gym_member.get()],
            "gym_id": self.gym_ids[self.gym_location.get()],
            "staff_id": self.staff_member_ids[self.staff_member.get()],
            "appointment_type": AppointmentType(self.appointment_type.get()),
            "schedule_date": self.schedule_date_entry.get(),
            "duration": self.duration.get()
        }

        success, message, appointment = self.appointment_service.create(data)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Appointment created successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()