from tkinter import ttk, messagebox

from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.presentation_layer.appointment_management.create_appointment_form import CreateAppointmentForm


class AppointmentTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.appointment_service = AppointmentService()
        self.gym_service = GymService()
        self.staff_member_service = StaffMemberService()
        self.gym_member_service = GymMemberService()

        self.action_frame = ttk.Frame(self)

        # Configuring tree columns to match appointment attributes
        self.tree = ttk.Treeview(self, columns=(
            'ID', 'Member', 'Gym', 'Staff', 'Appointment Type',
            'Scheduled Date', 'Status', 'Duration'
        ), show='headings')

        # Setting column headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Member', text='Member')
        self.tree.heading('Gym', text='Gym')
        self.tree.heading('Staff', text='Staff')
        self.tree.heading('Appointment Type', text='Appointment Type')
        self.tree.heading('Scheduled Date', text='Scheduled Date')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Duration', text='Duration')

        # Action buttons
        self.create_button = ttk.Button(
            self.action_frame,
            text="Create Appointment",
            command=self.create_appointment
        )
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(
            self.action_frame,
            text="Update Appointment",
            command=self.update_appointment
        )
        self.update_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(
            self.action_frame,
            text="Delete Appointment",
            command=self.delete_appointment
        )
        self.delete_button.pack(side='left', padx=5)

        self.action_frame.pack(fill='x', pady=5)

        # Tree and scrollbar setup
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_data(self):
        # Clear existing tree data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch all appointments
        appointments = self.appointment_service.get_all()

        # Populate tree
        for appointment in appointments:
            # Fetch member details
            success, message, member = self.gym_member_service.get_by_id(appointment.member_id)
            member_name = f"{member.first_name} {member.last_name}" if success else "Unknown Member"

            # Fetch gym details
            success, message, gym = self.gym_service.get_gym_by_id(appointment.gym_id)
            gym_location = gym.location if success else "Unknown Gym"

            # Fetch staff details
            success, message, staff = self.staff_member_service.get_by_id(appointment.staff_id)
            staff_name = f"{staff.first_name} {staff.last_name}" if success else "Unknown Staff"

            self.tree.insert('', 'end', values=(
                appointment.id,
                member_name,
                gym_location,
                staff_name,
                appointment.appointment_type.value,
                appointment.scheduled_date,
                appointment.status.value,
                appointment.duration
            ))

    def create_appointment(self):
        CreateAppointmentForm(
            self,
            self.gym_service,
            self.staff_member_service,
            self.gym_member_service,
            self.appointment_service,
            self.refresh_data
        )

    def update_appointment(self):
        pass

    def delete_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to delete")
            return

        # Get appointment ID from selected item
        appointment_data = self.tree.item(selected_item[0], 'values')
        appointment_id = appointment_data[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to delete the appointment"):
            success, message = self.appointment_service.delete(appointment_id)

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "Successfully deleted appointment")
                self.refresh_data()