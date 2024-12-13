from tkinter import ttk, messagebox

from src.business_layer.script.export_script import ExportScript


class ExportTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.export_script = ExportScript()
        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        # Buttons
        self.export_button = ttk.Button(self.action_frame, text="Export Data", command=self.export_data)
        self.export_button.pack(side='left', padx=5)

    def export_data(self):
        if messagebox.askyesno("Export Data", "Are you sure you want to export existing data?"):
            success, message = self.export_script.export()

            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)


