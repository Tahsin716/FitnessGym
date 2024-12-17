from tkinter import ttk

from src.business_layer.services.attendance_service import AttendanceService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.gym_service import GymService
from src.business_layer.services.zone_service import ZoneService
from src.business_layer.utils.common import Common
from src.presentation_layer.attendance_management.create_attendance_form import CreateAttendanceForm


class AttendanceTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.__attendance_service = AttendanceService()
        self.__gym_service = GymService()
        self.__zone_service = ZoneService()
        self.__gym_member_service = GymMemberService()

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        self.create_attendance_button = ttk.Button(self.action_frame, text="Create Attendance", command=self.create_attendance)
        self.create_attendance_button.pack(side='left', padx=5)

        self.tree = ttk.Treeview(self, columns=(
            'ID', 'Member Name', 'Gym Location', 'Zone Type', 'Check-in Time', 'Check-out Time', 'Duration'
        ), show='headings')

        columns_config = [
            ('ID', 50),
            ('Member Name', 200),
            ('Gym Location', 150),
            ('Zone Type', 100),
            ('Check-in Time', 100),
            ('Check-out Time', 100),
            ('Duration', 100)
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

        attendances = self.__attendance_service.get_all()

        for attendance in attendances:
            success, _, member = self.__gym_member_service.get_by_id(attendance.member_id)
            member_name = f"{member.first_name} {member.last_name}" if success else "Unknown"

            _, _, gym = self.__gym_service.get_gym_by_id(attendance.gym_id)
            _, _, zone = self.__zone_service.get_zone_by_id(attendance.zone_id)
            gym_location = gym.location if gym else "Unknown"
            zone_type = zone.zone_type.value if zone else "Unknown"

            self.tree.insert('', 'end', values=(
                attendance.id,
                member_name,
                gym_location,
                zone_type,
                attendance.checkin_time,
                attendance.checkout_time,
                Common.convert_minutes_to_hours_and_minutes_str(attendance.duration)
            ))

    def create_attendance(self):
        CreateAttendanceForm(
            self,
            self.__attendance_service,
            self.__gym_service,
            self.__gym_member_service,
            self.__zone_service,
            self.refresh_data
        )