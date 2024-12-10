from tkinter import ttk, messagebox

from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.subscription_service import SubscriptionService


class SubscriptionTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Configure grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.subscription_service = SubscriptionService()
        self.gym_member_service = GymMemberService()

        # Action Frame
        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        # Buttons
        self.create_button = ttk.Button(
            self.action_frame,
            text="Create Subscription",
            command=self.create_subscription
        )
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(
            self.action_frame,
            text="Update Subscription",
            command=self.update_subscription
        )
        self.update_button.pack(side='left', padx=5)

        self.cancel_button = ttk.Button(
            self.action_frame,
            text="Cancel Subscription",
            command=self.cancel_subscription
        )
        self.cancel_button.pack(side='left', padx=5)

        # Treeview with Columns
        self.tree = ttk.Treeview(self, columns=(
            'ID', 'Member', 'Plan', 'Monthly Rate', 'Payment Method',
            'Discount', 'Loyalty Points', 'Status'
        ), show='headings')

        # Configure column headings and widths
        columns_config = [
            ('ID', 50),
            ('Member', 150),
            ('Plan', 100),
            ('Monthly Rate', 100),
            ('Payment Method', 120),
            ('Discount', 80),
            ('Loyalty Points', 100),
            ('Status', 80)
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

        # Initial data refresh
        self.refresh_data()

    def refresh_data(self):
        # Clear existing tree data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch all subscriptions
        subscriptions = self.subscription_service.get_all()

        # Populate tree
        for subscription in subscriptions:
            # Fetch member details
            success, message, member = self.gym_member_service.get_by_id(subscription.member_id)
            member_name = f"{member.first_name} {member.last_name}" if success else "Unknown Member"

            self.tree.insert('', 'end', values=(
                subscription.id,
                member_name,
                subscription.subscription_plan.value,
                f"${subscription.monthly_rate:.2f}",
                subscription.payment_method.value,
                f"{subscription.discount}%",
                subscription.loyalty_points,
                "Active" if subscription.active else "Inactive"
            ))

    def create_subscription(self):
        pass

    def update_subscription(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a subscription to update")
            return

        # Get subscription data from selected item
        subscription_data = self.tree.item(selected_item[0], 'values')

        # Create a dictionary with subscription details
        update_data = {
            'id': subscription_data[0],
            'member': subscription_data[1],
            'subscription_plan': subscription_data[2],
            'payment_method': subscription_data[4],
            'discount': float(subscription_data[5].replace('%', '')),
            'loyalty_points': int(subscription_data[6])
        }

        pass

    def cancel_subscription(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a subscription to cancel")
            return

        # Get subscription ID from selected item
        subscription_data = self.tree.item(selected_item[0], 'values')
        subscription_id = subscription_data[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this subscription"):
            success, message = self.subscription_service.cancel(subscription_id)

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "Successfully canceled subscription")
                self.refresh_data()