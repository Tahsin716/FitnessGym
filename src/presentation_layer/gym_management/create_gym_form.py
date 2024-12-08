import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.gym_service import GymService


class CreateGymFrom(tk.Toplevel):
    def __init__(self, parent, gym_service : GymService, callback):
        super().__init__(parent)
        self.gym_service = gym_service
        self.callback = callback

        self.title("Create Gym")
        self.geometry("400x300")

        self.location = tk.StringVar()
        self.post_code = tk.StringVar()
        self.address = tk.StringVar()
        self.phone_number = tk.StringVar()
        self.email = tk.StringVar()

        ttk.Label(self, text="Location").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.location).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Post Code").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.post_code).grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Address").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.address).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text="Phone Number").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.phone_number).grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self, text="Email").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.email).grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(self, text="Save", command=self.save_gym).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=5, column=1, padx=10, pady=10)

    def save_gym(self):
        location = self.location.get()
        post_code = self.post_code.get()
        address = self.address.get()
        phone_number = self.phone_number.get()
        email = self.email.get()

        data = {
            "location": location,
            "post_code": post_code,
            "address": address,
            "phone_number": phone_number,
            "email": email
        }

        success, message, gym = self.gym_service.create(data)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Gym created successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()
