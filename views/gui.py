import tkinter as tk
from tkinter import ttk # styles properly according to user's OS
from tkinter import messagebox
from views.tela_login import TelaLogin
from views.tela_inicial import TelaInicial

class App(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.title("Shadow Notes")
        self.geometry("800x600")
        self.frames = {}

        for nome, Frame in {"tela login": TelaLogin, "tela inicial": TelaInicial}.items(): # adicionar todas as telas nesse dicionario
            frame = Frame(master = self, controller = self, db = self.db) # observa aqui
            self.frames[nome] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_screen("tela login")
    

    def show_screen(self, screen):
        frame = self.frames[screen]
        frame.tkraise()
