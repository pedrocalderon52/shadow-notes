import tkinter as tk
from tkinter import ttk # styles properly according to user's OS
from tkinter import messagebox
from views.tela_inicial import TelaInicial

class App(tk.Tk):
    def __init__(self, db):
        self.db = db

        super().__init__()
        self.title("Shadow Notes")
        self.geometry("400x300")
        self.frames = {}

        for nome, Frame in {"tela inicial": TelaInicial}.items(): # adicionar todas as telas nesse dicionario
            frame = Frame(master = self, controller = self, db = self.db) # observa aqui
            self.frames[Frame] = frame
            frame.pack()

        self.show_screen(TelaInicial)
    

    def show_screen(self, screen):
        frame = self.frames[screen]
        frame.tkraise()
