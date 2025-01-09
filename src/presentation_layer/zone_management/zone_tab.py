from tkinter import ttk, messagebox

from src.business_layer.services.gym_service import GymService
from src.business_layer.services.staff_member_service import StaffMemberService
from src.business_layer.services.zone_service import ZoneService
from src.presentation_layer.zone_management.create_zone_form import CreateZoneForm
from src.presentation_layer.zone_management.update_zone_form import UpdateZoneForm


class ZoneTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.zone_service = ZoneService()
        self.gym_service = GymService()
        self.staff_member_service = StaffMemberService()

        self.action_frame = ttk.Frame(self)

        self.tree = ttk.Treeview(self, columns=('ID', 'Gym Location', 'Zone Type', 'Attendant'),
                                 show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Gym Location', text='Gym Location')
        self.tree.heading('Zone Type', text='Zone Type')
        self.tree.heading('Attendant', text='Attendant')

        self.create_button = ttk.Button(self.action_frame, text="Create Zone", command=self.create_zone, style="Create.TButton")
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(self.action_frame, text="Update Zone", command=self.update_zone, style="Update.TButton")
        self.update_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(self.action_frame, text="Delete Zone", command=self.delete_zone, style="Delete.TButton")
        self.delete_button.pack(side='left', padx=5)

        self.action_frame.pack(fill='x', pady=5)

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_data(self):
        zones = self.zone_service.get_all_zones()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for zone in zones:
            success, message, gym =  self.gym_service.get_gym_by_id(zone.gym_id)
            success, message, staff = self.staff_member_service.get_by_id(zone.attendant_id)


            self.tree.insert('', 'end', values=(zone.id, gym.location, zone.zone_type.value, f"{staff.first_name} {staff.last_name}"))


    def create_zone(self):
        CreateZoneForm(self, self.gym_service, self.staff_member_service, self.zone_service, self.refresh_data)

    def update_zone(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a zone to update")
            return

        zone_data = self.tree.item(selected_item[0], 'values')
        zone_id = zone_data[0]

        success, message, zone = self.zone_service.get_zone_by_id(zone_id)
        if not success:
            messagebox.showerror("Error", message)
            return

        UpdateZoneForm(
            self,
            zone,
            self.gym_service,
            self.staff_member_service,
            self.zone_service,
            self.refresh_data
        )

    def delete_zone(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a zone to delete")
            return

        zone_data = self.tree.item(selected_item[0], 'values')
        zone_id = zone_data[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to delete the zone"):
            success, message = self.zone_service.delete(zone_id)

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "Successfully deleted zone")
                self.refresh_data()


