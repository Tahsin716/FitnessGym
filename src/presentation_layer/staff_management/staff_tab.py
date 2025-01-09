from tkinter import ttk, messagebox

from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.presentation_layer.staff_management.create_staff_form import CreateStaffMemberForm
from src.presentation_layer.staff_management.update_staff_form import UpdateStaffMemberForm


class StaffMemberTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.staff_member_service = StaffMemberService()
        self.gym_service = GymService()

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        self.create_button = ttk.Button(self.action_frame, text="Create Staff Member", command=self.create_staff_member, style="Create.TButton")
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(self.action_frame, text="Update Staff Member", command=self.update_staff_member, style="Update.TButton")
        self.update_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(self.action_frame, text="Delete Staff Member", command=self.delete_staff_member, style="Delete.TButton")
        self.delete_button.pack(side='left', padx=5)

        self.tree = ttk.Treeview(self, columns=(
            'ID', 'First Name', 'Last Name', 'Email',
            'Phone Number', 'Role', 'Gym Location'
        ), show='headings')

        columns_config = [
            ('ID', 50),
            ('First Name', 100),
            ('Last Name', 100),
            ('Email', 200),
            ('Phone Number', 120),
            ('Role', 100),
            ('Gym Location', 150)
        ]

        for col, width in columns_config:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center', stretch=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        scrollbar.grid(row=1, column=1, sticky='ns')

        self.refresh_data()

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        staff_members = self.staff_member_service.get_all()

        for staff_member in staff_members:
            success, message, gym = self.gym_service.get_gym_by_id(staff_member.gym_id)

            self.tree.insert('', 'end', values=(
                staff_member.id, 
                staff_member.first_name, 
                staff_member.last_name, 
                staff_member.email, 
                staff_member.phone_number, 
                staff_member.role.value, 
                gym.location
            ))

    def create_staff_member(self):
        CreateStaffMemberForm(self, self.staff_member_service, self.gym_service  ,self.refresh_data)

    def update_staff_member(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a staff member to update")
            return

        data = self.tree.item(selected_item[0], 'values')
        UpdateStaffMemberForm(self, self.staff_member_service, self.gym_service , data, self.refresh_data)

    def delete_staff_member(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a staff member to delete")
            return

        user_data = self.tree.item(selected_item[0], 'values')
        _id = user_data[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this staff member?"):
            success, message = self.staff_member_service.delete(_id)

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "Staff member successfully deleted")
                self.refresh_data()