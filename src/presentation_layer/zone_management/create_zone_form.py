import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.business_layer.services.zone_service import ZoneService
from src.data_layer.enum.role import Role
from src.data_layer.enum.zone_type import ZoneType


class CreateZoneForm(tk.Toplevel):
    def __init__(self, parent, gym_service: GymService,
                 staff_member_service: StaffMemberService,
                 zone_service: ZoneService,
                 callback):
        super().__init__(parent)
        self.gym_service = gym_service
        self.staff_member_service = staff_member_service
        self.zone_service = zone_service
        self.callback = callback

        self.title("Create Zone")
        self.geometry("400x300")

        self.gym_location = tk.StringVar()
        self.zone_type = tk.StringVar()
        self.attendant = tk.StringVar()

        gyms = self.gym_service.get_all_gyms()
        self.gym_locations = [gym.location for gym in gyms]
        self.gym_ids = {gym.location: gym.id for gym in gyms}
        self.attendant_ids = {}

        ttk.Label(self, text="Gym Location").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.gym_location_dropdown = ttk.Combobox(
            self,
            textvariable=self.gym_location,
            values=self.gym_locations,
            state="readonly"
        )
        self.gym_location_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.gym_location_dropdown.bind('<<ComboboxSelected>>', self.on_gym_location_selected)

        ttk.Label(self, text="Zone Type").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.zone_type_dropdown = ttk.Combobox(
            self,
            textvariable=self.zone_type,
            values=[zt.value for zt in ZoneType],
            state="readonly"
        )
        self.zone_type_dropdown.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Attendant").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.attendant_dropdown = ttk.Combobox(
            self,
            textvariable=self.attendant,
            state="disabled"
        )
        self.attendant_dropdown.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(self, text="Save", command=self.save_zone).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=3, column=1, padx=10, pady=10)

    def on_gym_location_selected(self, event=None):
        self.attendant.set('')

        selected_gym_location = self.gym_location.get()
        selected_gym_id = self.gym_ids[selected_gym_location]

        attendants = self.staff_member_service.get_all_by_role_and_gym(Role.ATTENDANT, selected_gym_id)

        if attendants:
            attendant_names = [f"{staff.first_name} {staff.last_name}" for staff in attendants]
            self.attendant_ids = {f"{staff.first_name} {staff.last_name}": staff.id for staff in attendants}

            self.attendant_dropdown['values'] = attendant_names
            self.attendant_dropdown['state'] = 'readonly'
        else:
            self.attendant_dropdown['values'] = []
            self.attendant_dropdown['state'] = 'disabled'

    def save_zone(self):
        if not self.gym_location.get():
            messagebox.showerror("Error", "Please select a gym location")
            return

        if not self.zone_type.get():
            messagebox.showerror("Error", "Please select a zone type")
            return

        if not self.attendant.get():
            messagebox.showerror("Error", "Please select an attendant")
            return

        data = {
            "gym_id": self.gym_ids[self.gym_location.get()],
            "zone_type": ZoneType(self.zone_type.get()),
            "attendant_id": self.attendant_ids[self.attendant.get()]
        }

        success, message, zone = self.zone_service.create(data)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Zone created successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()