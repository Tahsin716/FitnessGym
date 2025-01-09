import tkinter as tk
from tkinter import ttk

from src.presentation_layer.main_page import MainPage


class Application:

    def __init__(self):
        root = tk.Tk()
        root.title("Fitness Gym")
        root.lift()
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - 50, root.winfo_screenheight() - 50))

        container = ttk.Frame()
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in ([MainPage]):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.setup_button_styles()
        self.show_frame("MainPage")
        root.mainloop()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def setup_button_styles(self):
        style = ttk.Style()

        style.configure(
            'Create.TButton',
            foreground='#119e24'
        )

        style.configure(
            'Update.TButton',
            foreground='#052df5'
        )

        style.configure(
            'Complete.TButton',
            foreground='#673AB7'
        )

        style.configure(
            'Cancel.TButton',
            foreground='#a6a39c'
        )

        style.configure(
            'Delete.TButton',
            foreground='#f44336'
        )


