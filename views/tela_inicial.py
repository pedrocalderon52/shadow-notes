import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TelaInicial(tk.Frame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.db = db
        self.controller = controller

        tk.Label(self, text = "TELA INICIAL").pack(pady=5)

        print("Tela inicial inicializada")


