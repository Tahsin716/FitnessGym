import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.gym_member_service import GymMemberService
from src.data_layer.enum.membership_type import MembershipType


class UpdateGymMemberForm(tk.Toplevel):
    def __init__(self, parent, gym_member_service: GymMemberService, member_data, callback):
        super().__init__(parent)
        self.gym_member_service = gym_member_service
        self.member_data = member_data
        self.callback = callback

        self.title("Update Gym Member")
        self.geometry("400x500")

        # Variables to store form data
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone_number = tk.StringVar()
        self.membership_type = tk.StringVar()
        self.height = tk.StringVar()
        self.weight = tk.StringVar()

        # Load existing member data
        self.load_member_data()

        # First Name
        ttk.Label(self, text="First Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.first_name).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Last Name
        ttk.Label(self, text="Last Name").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.last_name).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Email
        ttk.Label(self, text="Email").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.email).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Phone Number
        ttk.Label(self, text="Phone Number").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.phone_number).grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Membership Type
        ttk.Label(self, text="Membership Type").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        membership_dropdown = ttk.Combobox(
            self,
            textvariable=self.membership_type,
            values=[mt.value for mt in MembershipType],
            state="readonly"
        )
        membership_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Height
        ttk.Label(self, text="Height (cm)").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.height).grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Weight
        ttk.Label(self, text="Weight (kg)").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.weight).grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # Buttons
        ttk.Button(self, text="Update", command=self.update_member).grid(row=7, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=7, column=1, padx=10, pady=10)

        # Configure column weights
        self.grid_columnconfigure(1, weight=1)

    def load_member_data(self):
        self.first_name.set(self.member_data[1])
        self.last_name.set(self.member_data[2])
        self.email.set(self.member_data[3])
        self.phone_number.set(self.member_data[4])
        self.membership_type.set(self.member_data[5])
        self.height.set(str(self.member_data[6]))
        self.weight.set(str(self.member_data[7]))

    def update_member(self):
        data = {
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "email": self.email.get(),
            "phone_number": self.phone_number.get(),
            "membership_type": MembershipType(self.membership_type.get()),
            "height": self.height.get(),
            "weight": self.weight.get()
        }

        success, message, member = self.gym_member_service.update(self.member_data[0], data)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Gym Member updated successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()