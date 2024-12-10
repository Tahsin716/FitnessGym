from tkinter import ttk

from src.presentation_layer.appointment_management.appointment_tab import AppointmentTab
from src.presentation_layer.gym_management.gym_tab import GymTab
from src.presentation_layer.gym_member_managemet.gym_member_tab import GymMemberTab
from src.presentation_layer.payment_management.payment_tab import PaymentTab
from src.presentation_layer.staff_management.staff_tab import StaffMemberTab
from src.presentation_layer.subscription_management.subscription_tab import SubscriptionTab
from src.presentation_layer.zone_management.zone_tab import ZoneTab


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.notebook = ttk.Notebook(self)

        self.tabs = {
            "Gyms": GymTab(self.notebook),
            "Zones": ZoneTab(self.notebook),
            "Gym Member": GymMemberTab(self.notebook),
            "Staff Member": StaffMemberTab(self.notebook),
            "Appointment": AppointmentTab(self.notebook),
            "Subscription" : SubscriptionTab(self.notebook),
            "Payment" : PaymentTab(self.notebook)
        }

        for tab_name, tab_instance in self.tabs.items():
            self.notebook.add(tab_instance, text=tab_name)

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        self.notebook.pack(expand=True, fill='both')

    def on_tab_changed(self, event):
        current_tab_index = self.notebook.index(self.notebook.select())
        current_tab_name = self.notebook.tab(current_tab_index, "text")

        if current_tab_name in self.tabs:
            current_tab = self.tabs[current_tab_name]

            if hasattr(current_tab, 'refresh_data'):
                current_tab.refresh_data()