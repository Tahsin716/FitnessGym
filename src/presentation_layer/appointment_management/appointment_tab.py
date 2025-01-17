from tkinter import ttk, messagebox

from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.presentation_layer.appointment_management.create_appointment_form import CreateAppointmentForm
from src.presentation_layer.appointment_management.update_appointment_form import UpdateAppointmentForm


class AppointmentTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.appointment_service = AppointmentService()
        self.gym_service = GymService()
        self.staff_member_service = StaffMemberService()
        self.gym_member_service = GymMemberService()

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        self.create_button = ttk.Button(
            self.action_frame,
            text="Create Appointment",
            command=self.create_appointment,
            style="Create.TButton"
        )
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(
            self.action_frame,
            text="Update Appointment",
            command=self.update_appointment,
            style="Update.TButton"
        )
        self.update_button.pack(side='left', padx=5)

        self.complete_button = ttk.Button(
            self.action_frame,
            text="Complete Appointment",
            command=self.complete_appointment,
            style="Complete.TButton"
        )
        self.complete_button.pack(side='left', padx=5)

        self.cancel_button = ttk.Button(
            self.action_frame,
            text="Cancel Appointment",
            command=self.cancel_appointment,
            style="Cancel.TButton"
        )
        self.cancel_button.pack(side='left', padx=5)

        self.tree = ttk.Treeview(self, columns=(
            'ID', 'Member', 'Gym', 'Staff', 'Appointment Type',
            'Scheduled Date', 'Status', 'Duration', 'Payment Status'
        ), show='headings')

        columns_config = [
            ('ID', 50),
            ('Member', 150),
            ('Gym', 100),
            ('Staff', 150),
            ('Appointment Type', 150),
            ('Scheduled Date', 120),
            ('Status', 100),
            ('Duration', 100),
            ('Payment Status', 100)
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

        appointments = self.appointment_service.get_all()

        for appointment in appointments:
            success, message, member = self.gym_member_service.get_by_id(appointment.member_id)
            member_name = f"{member.first_name} {member.last_name}" if success else "Unknown Member"

            success, message, gym = self.gym_service.get_gym_by_id(appointment.gym_id)
            gym_location = gym.location if success else "Unknown Gym"

            success, message, staff = self.staff_member_service.get_by_id(appointment.staff_id)
            staff_name = f"{staff.first_name} {staff.last_name}" if success else "Unknown Staff"

            self.tree.insert('', 'end', values=(
                appointment.id,
                member_name,
                gym_location,
                staff_name,
                appointment.appointment_type.value,
                appointment.scheduled_date.strftime('%Y-%m-%d'),
                appointment.status.value,
                appointment.duration,
               "Paid" if appointment.is_paid else "Pending"
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
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to update")
            return

        appointment_data = self.tree.item(selected_item[0], 'values')

        update_data = {
            'id': appointment_data[0],
            'member': appointment_data[1],
            'gym': appointment_data[2],
            'staff': appointment_data[3],
            'appointment_type': appointment_data[4],
            'scheduled_date': appointment_data[5],
            'duration': appointment_data[7]
        }

        UpdateAppointmentForm(
            self,
            self.gym_service,
            self.staff_member_service,
            self.gym_member_service,
            self.appointment_service,
            update_data,
            self.refresh_data
        )

    def complete_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to complete")
            return

        appointment_data = self.tree.item(selected_item[0], 'values')
        appointment_id = appointment_data[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to complete the appointment"):
            success, message = self.appointment_service.complete(appointment_id)

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "Successfully completed appointment")
                self.refresh_data()

    def cancel_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return

        appointment_data = self.tree.item(selected_item[0], 'values')
        appointment_id = appointment_data[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to cancel the appointment"):
            success, message = self.appointment_service.cancel(appointment_id)

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "Successfully cancelled appointment")
                self.refresh_data()