import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.data_layer.enum.role import Role


class CreateStaffMemberForm(tk.Toplevel):
    def __init__(self, parent, staff_member_service: StaffMemberService, gym_service: GymService, callback):
        super().__init__(parent)
        self.staff_member_service = staff_member_service
        self.gym_service = gym_service
        self.callback = callback

        self.title("Create Staff Member")
        self.geometry("400x450")

        # StringVars for form fields
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone_number = tk.StringVar()
        self.role = tk.StringVar()

        # Gym selection
        self.selected_gym_id = tk.StringVar()
        self.gym_locations = self.get_gym_locations()

        # First Name
        ttk.Label(self, text="First Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.first_name).grid(row=0, column=1, padx=10, pady=5)

        # Last Name
        ttk.Label(self, text="Last Name").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.last_name).grid(row=1, column=1, padx=10, pady=5)

        # Email
        ttk.Label(self, text="Email").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.email).grid(row=2, column=1, padx=10, pady=5)

        # Phone Number
        ttk.Label(self, text="Phone Number").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.phone_number).grid(row=3, column=1, padx=10, pady=5)

        # Role
        ttk.Label(self, text="Role").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        role_dropdown = ttk.Combobox(self, textvariable=self.role,
                                     values=[role.value for role in Role],
                                     state="readonly")
        role_dropdown.grid(row=4, column=1, padx=10, pady=5)

        # Gym Location
        ttk.Label(self, text="Gym Location").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        gym_dropdown = ttk.Combobox(self, values=list(self.gym_locations.keys()),
                                    state="readonly")
        gym_dropdown.grid(row=5, column=1, padx=10, pady=5)

        # Bind the selection to set the gym ID
        gym_dropdown.bind('<<ComboboxSelected>>', self.on_gym_select)

        # Save and Cancel Buttons
        ttk.Button(self, text="Save", command=self.save_staff_member).grid(row=6, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=6, column=1, padx=10, pady=10)

    def get_gym_locations(self):
        # Fetch gyms and create a dictionary of location: id
        gyms = self.gym_service.get_all_gyms()
        return {gym.location: gym.id for gym in gyms}

    def on_gym_select(self, event):
        # Set the selected gym ID based on the location
        selected_location = event.widget.get()
        self.selected_gym_id.set(self.gym_locations[selected_location])

    def save_staff_member(self):
        # Collect data from form fields
        data = {
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "email": self.email.get(),
            "phone_number": self.phone_number.get(),
            "role": Role(self.role.get()),
            "gym_id": self.selected_gym_id.get()
        }

        # Validate all fields are filled
        for key, value in data.items():
            if not value:
                messagebox.showerror("Error", f"{key.replace('_', ' ').title()} cannot be empty")
                return

        # Attempt to create staff member
        success, message, staff_member = self.staff_member_service.create(data)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Staff member created successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()