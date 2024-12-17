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

        self.show_frame("MainPage")
        root.mainloop()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


