from tkinter import ttk, messagebox

from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.presentation_layer.staff_management.create_staff_form import CreateStaffMemberForm
from src.presentation_layer.staff_management.update_staff_form import UpdateStaffMemberForm


class StaffMemberTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.staff_member_service = StaffMemberService()
        self.gym_service = GymService()

        self.action_frame = ttk.Frame(self)

        self.tree = ttk.Treeview(self, columns=('ID', 'First Name', 'Last Name', 'Email', 'Phone Number', 'Role', 'Gym Location'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('First Name', text='First Name')
        self.tree.heading('Last Name', text='Last Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Phone Number', text='Phone Number')
        self.tree.heading('Role', text='Role')
        self.tree.heading('Gym Location', text='Gym Location')

        self.create_button = ttk.Button(self.action_frame, text="Create Staff Member", command=self.create_staff_member)
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(self.action_frame, text="Update Staff Member", command=self.update_staff_member)
        self.update_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(self.action_frame, text="Delete Staff Member", command=self.delete_staff_member)
        self.delete_button.pack(side='left', padx=5)

        self.action_frame.pack(fill='x', pady=5)

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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