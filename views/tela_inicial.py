import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import re # It helps to search for patterns in strings


class TelaInicial(ttk.Frame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.db = db

        # Username entry label
        ttk.Label(self, text="User:").pack(pady=10)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()

        # Password entry label
        ttk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        # Login button
        ttk.Button(self, text="Login", command=self.login).pack(pady=15)

        # Sign up button
        ttk.Button(self, text="Sign Up", command=self.sign_up).pack(pady=15) # command = lambda: controller.show_screen("secundaria")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.db.login_user(username, password)
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
        except:
            messagebox.showerror("Login Failed", "Invalid username or password.")
                

                
    def valid_password(self, password) -> bool:
        """This function checks if there is at least one uppercase letter and one special character in the password."""
        has_upper = re.search(r"[A-Z]", password)
        has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        return bool(has_upper and has_special)


    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
        elif not self.valid_password(password):
            messagebox.showerror("Weak Password", "Password must contain at least one uppercase letter and one special character.")
        else:
            try:
                self.db.sign_user(username, password)
                messagebox.showinfo("Registration Successful", f"Account created for {username}!")
            except:
                messagebox.showerror("User error", "Username already exists")


        