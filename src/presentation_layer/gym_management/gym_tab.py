from tkinter import ttk

from src.business_layer.services.gym_service import GymService
from src.presentation_layer.gym_management.create_gym_form import CreateGymFrom


class GymTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.gym_service = GymService()

        self.action_frame = ttk.Frame(self)

        self.tree = ttk.Treeview(self, columns=('ID', 'Location', 'Address', 'Post Code', 'Phone Number', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Address', text='Address')
        self.tree.heading('Post Code', text='Post Code')
        self.tree.heading('Phone Number', text='Phone Number')
        self.tree.heading('Email', text='Email')

        self.create_button = ttk.Button(self.action_frame, text="Create Gym", command=self.create_gym)
        self.create_button.pack(side='left', padx=5)

        self.update_button = ttk.Button(self.action_frame, text="Update Gym", command=self.update_gym)
        self.update_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(self.action_frame, text="Delete Gym", command=self.delete_gym)
        self.delete_button.pack(side='left', padx=5)

        self.action_frame.pack(fill='x', pady=5)

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_data(self):
        gyms = self.gym_service.get_all_gyms()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for gym in gyms:
            self.tree.insert('', 'end', values=(gym.id, gym.location, gym.address, gym.post_code, gym.phone_number, gym.email))

    def create_gym(self):
        CreateGymFrom(self, self.gym_service, self.refresh_data)

    def update_gym(self):
        pass

    def delete_gym(self):
        pass
