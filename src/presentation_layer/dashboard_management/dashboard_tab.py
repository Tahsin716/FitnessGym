from tkinter import ttk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.business_layer.services.dashboard_service import DashboardService


class DashboardTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__dashboard_service = DashboardService()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.appointments_frame = ttk.LabelFrame(self, text="Appointments")
        self.appointments_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.subscriptions_frame = ttk.LabelFrame(self, text="Subscriptions")
        self.subscriptions_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.payments_frame = ttk.LabelFrame(self, text="Payments")
        self.payments_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.attendance_frame = ttk.LabelFrame(self, text="Attendance")
        self.attendance_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.__chart_info = {}

        self.refresh_data()

    def refresh_data(self):
        for item in self.__chart_info.values():
            item.destroy()

        appointment_data = self.__dashboard_service.get_current_month_appointment_data()
        subscription_data = self.__dashboard_service.get_current_month_subscription_data()
        payment_data = self.__dashboard_service.get_current_month_payment_data()
        attendance_data = self.__dashboard_service.get_current_month_attendance()

        self._create_pie_chart(
            self.appointments_frame,
            "Monthly Appointments",
            appointment_data,
            ['PersonalTraining', 'GroupClass', 'NutritionConsultant']
        )

        self._create_pie_chart(
            self.subscriptions_frame,
            "Monthly Subscriptions",
            subscription_data,
            ['Monthly', 'Quarterly', 'Annual']
        )

        self._create_numeric_display(
            self.payments_frame,
            "Monthly Payments",
            payment_data
        )

        self._create_attendance_display(
            self.attendance_frame,
            "Monthly Attendance",
            attendance_data
        )

    def _create_pie_chart(self, parent_frame, title, data, keys):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        if data['Total'] == 0:
            label = ttk.Label(parent_frame, text=f"No data to display for {title}")
            label.pack(expand=True, fill='both')
            return

        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)

        pie_data = [data.get(key, 0) for key in keys]
        ax.pie(pie_data, labels=keys, autopct='%1.1f%%')
        ax.set_title(title, fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill='both')

        self.__chart_info[title] = canvas_widget

        plt.close(fig)


    def _create_numeric_display(self, parent_frame, title, data):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        if data['Total'] == 0:
            label = ttk.Label(parent_frame, text=f"No data to display for {title}")
            label.pack(expand=True, fill='both')
            return

        frame = ttk.LabelFrame(parent_frame)
        frame.pack()

        ttk.Label(frame, text=f"Total Payments: {data['Total']}").pack()
        ttk.Label(frame, text=f"Total Amount: ${data['Amount']:,.2f}").pack()

    def _create_attendance_display(self, parent_frame, title, data):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        if data['Total'] == 0:
            label = ttk.Label(parent_frame, text=f"No data to display for {title}")
            label.pack(expand=True, fill='both')
            return

        frame = ttk.Frame(parent_frame)
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text=f"Total Attendances: {data['Total']}").pack()
        ttk.Label(frame, text=f"Popular Location: {data.get('PopularGymLocation', 'N/A')}").pack()
        ttk.Label(frame, text=f"Peak Hour: {data.get('PeakHour', 'N/A')}").pack()
        ttk.Label(frame, text=f"Total Duration: {data.get('TotalDuration', 'N/A')}").pack()
