from tkinter import ttk

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.notebook = ttk.Notebook(self)

        self.tabs = {
            #"Users": UserManagementTab(self.notebook),
            #"Expenses": ExpensesTab(self.notebook),
            #"Inventory": InventoryManagementTab(self.notebook),
            #"Sales": SalesTab(self.notebook),
            #"Sales Tracking": SalesTrackingTab(self.notebook),
            #"Reporting" : ReportingTab(self.notebook)
        }

        for tab_name, tab_instance in self.tabs.items():
            self.notebook.add(tab_instance, text=tab_name)

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        self.notebook.pack(expand=True, fill='both')

    def on_tab_changed(self, event):
        current_tab_index = self.notebook.index(self.notebook.select())
        current_tab_name = self.notebook.tab(current_tab_index, "text")

        if current_tab_name in self.tabs:
            current_tab = self.tabs[current_tab_name]

            if hasattr(current_tab, 'refresh_data'):
                current_tab.refresh_data()