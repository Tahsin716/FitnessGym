import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.attendance_service import AttendanceService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.zone_service import ZoneService


class CreateAttendanceForm(tk.Toplevel):
    def __init__(self, parent, attendance_service: AttendanceService, gym_service: GymService,
                 gym_member_service: GymMemberService, zone_service: ZoneService, callback):
        super().__init__(parent)

        self.attendance_service = attendance_service
        self.gym_service = gym_service
        self.gym_member_service = gym_member_service
        self.zone_service = zone_service
        self.callback = callback

        self.title("Create Attendance")
        self.geometry("500x400")

        self.selected_gym = tk.StringVar()
        self.selected_member = tk.StringVar()
        self.selected_zone = tk.StringVar()
        self.checkin_time = tk.StringVar()
        self.checkout_time = tk.StringVar()

        ttk.Label(self, text="Select Gym").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.gym_dropdown = ttk.Combobox(self, textvariable=self.selected_gym, state="readonly")
        self.gym_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self, text="Select Member").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.member_dropdown = ttk.Combobox(self, textvariable=self.selected_member, state="readonly")
        self.member_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self, text="Select Workout Zone").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.zone_dropdown = ttk.Combobox(self, textvariable=self.selected_zone, state="disabled")
        self.zone_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")


        ttk.Label(self, text="Check-in Time (HH:MM)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.checkin_entry = ttk.Entry(self, textvariable=self.checkin_time)
        self.checkin_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self, text="Check-out Time (HH:MM)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.checkout_entry = ttk.Entry(self, textvariable=self.checkout_time)
        self.checkout_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(self, text="Create", command=self.create_attendance).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.destroy).grid(row=5, column=1, padx=10, pady=10)

        self.populate_gyms()

        self.gym_dropdown.bind('<<ComboboxSelected>>', self.on_gym_select)
        self.member_dropdown.bind('<<ComboboxSelected>>', self.on_member_select)

    def populate_gyms(self):
        gyms = self.gym_service.get_all_gyms()
        gym_list = [f"{gym.location} ({gym.id})" for gym in gyms]
        self.gym_dropdown['values'] = gym_list

    def on_gym_select(self, event):
        if not self.selected_gym.get():
            return

        self.selected_zone.set('')

        gym_id = self.selected_gym.get().split('(')[1].strip(')')

        members = self.gym_member_service.get_all()
        member_list = [f"{member.first_name} {member.last_name} ({member.id})" for member in members]
        self.member_dropdown['values'] = member_list

        zones = self.zone_service.get_zones_by_gym_id(gym_id)
        zone_list = [f"{zone.zone_type.value} ({zone.id})" for zone in zones]

        if zone_list:
            self.zone_dropdown['values'] = zone_list
            self.zone_dropdown['state'] = 'readonly'
        else:
            self.zone_dropdown['values'] = []
            self.zone_dropdown['state'] = 'disabled'

    def on_member_select(self, event):
        pass

    def create_attendance(self):
        if not all([self.selected_gym.get(), self.selected_member.get(),
                    self.selected_zone.get(), self.checkin_time.get(),
                    self.checkout_time.get()]):
            messagebox.showerror("Error", "All fields are required")
            self.focus()
            return

        gym_id = self.selected_gym.get().split('(')[1].strip(')')
        member_id = self.selected_member.get().split('(')[1].strip(')')
        zone_id = self.selected_zone.get().split('(')[1].strip(')')

        attendance_data = {
            'gym_id': gym_id,
            'member_id': member_id,
            'zone_id': zone_id,
            'checkin_time': self.checkin_time.get(),
            'checkout_time': self.checkout_time.get()
        }

        success, message, _ = self.attendance_service.create(attendance_data)

        if success:
            messagebox.showinfo("Success", "Attendance created successfully")
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", message)
            self.focus()