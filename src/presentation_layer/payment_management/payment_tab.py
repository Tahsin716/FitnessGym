from tkinter import ttk

from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.payment_service import PaymentService
from src.business_layer.services.subscription_service import SubscriptionService


class PaymentTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Configure grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Services
        self.gym_member_service = GymMemberService()
        self.subscription_service = SubscriptionService()
        self.appointment_service = AppointmentService()
        self.payment_service = PaymentService()

        # Action Frame
        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        # Buttons
        self.create_payment_button = ttk.Button(self.action_frame, text="Create Payment", command=self.create_payment)
        self.create_payment_button.pack(side='left', padx=5)

        # Treeview with Scrollbar
        self.tree = ttk.Treeview(self, columns=(
            'ID', 'Member Name', 'Total Amount', 'Payment Method', 'Date'
        ), show='headings')

        # Configure column headings and widths
        columns_config = [
            ('ID', 50),
            ('Member Name', 200),
            ('Total Amount', 100),
            ('Payment Method', 150),
            ('Date', 150)
        ]

        for col, width in columns_config:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center', stretch=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid placement of Treeview and Scrollbar
        self.tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        scrollbar.grid(row=1, column=1, sticky='ns')

        self.refresh_data()

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        payments = self.payment_service.get_all()

        for payment in payments:
            member_success, member_message, member = self.gym_member_service.get_by_id(payment.member_id)
            member_name = f"{member.first_name} {member.last_name}" if member_success else "Unknown"

            self.tree.insert('', 'end', values=(
                payment.id,
                member_name,
                f"${payment.amount:.2f}",
                payment.payment_method.value,
                payment.create_date.strftime("%Y-%m-%d %H:%M:%S")
            ))

    def create_payment(self):
        pass