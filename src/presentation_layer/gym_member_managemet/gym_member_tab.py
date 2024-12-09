from tkinter import ttk, messagebox

from src.business_layer.services.gym_member_service import GymMemberService
from src.presentation_layer.gym_member_managemet.create_gym_member_form import CreateGymMemberForm


class GymMemberTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Configure grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.gym_member_service = GymMemberService()

        # Action Frame
        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        # Buttons
        self.create_button = ttk.Button(self.action_frame, text="Create Member", command=self.create_member)
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(self.action_frame, text="Update Member", command=self.update_member)
        self.update_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(self.action_frame, text="Delete Member", command=self.delete_member)
        self.delete_button.pack(side='left', padx=5)

        # Treeview with Scrollbar
        self.tree = ttk.Treeview(self, columns=(
            'ID', 'First Name', 'Last Name', 'Email',
            'Phone Number', 'Membership Type', 'Height', 'Weight'
        ), show='headings')

        # Configure column headings and widths
        columns_config = [
            ('ID', 50),
            ('First Name', 100),
            ('Last Name', 100),
            ('Email', 200),
            ('Phone Number', 120),
            ('Membership Type', 120),
            ('Height', 70),
            ('Weight', 70)
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
        members = self.gym_member_service.get_all()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for member in members:
            self.tree.insert('', 'end', values=(
                member.id,
                member.first_name,
                member.last_name,
                member.email,
                member.phone_number,
                member.membership_type.value,
                member.height,
                member.weight
            ))

    def create_member(self):
        CreateGymMemberForm(self, self.gym_member_service, self.refresh_data)

    def update_member(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a member to update")
            return
        pass

    def delete_member(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a member to delete")
            return
        pass