import tkinter as tk
from tkinter import ttk # styles properly according to user's OS
from tkinter import messagebox
import re # It helps to search for patterns in strings
from db import DB


db: DB = DB()

def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        db.login_user(username, password)
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
    except:
        messagebox.showerror("Login Failed", "Invalid username or password.")


        

        
def valid_password(password) -> bool:
    """This function checks if there is at least one uppercase letter and one special character in the password."""
    has_upper = re.search(r"[A-Z]", password)
    has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    return bool(has_upper and has_special)


def sign_up():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")
    elif not valid_password(password):
        messagebox.showerror("Weak Password", "Password must contain at least one uppercase letter and one special character.")
    else:
        try:
            db.sign_user(username, password)
            messagebox.showinfo("Registration Successful", f"Account created for {username}!")
        except:
            messagebox.showerror("User error", "Username already exists")


# Create main window
root = tk.Tk()
root.title("Login Page")
root.geometry("400x300")
root.resizable(False, False)

# Username entry label
ttk.Label(root, text="Username:").pack(pady=5)
username_entry = ttk.Entry(root)
username_entry.pack()

# Password entry label
ttk.Label(root, text="Password:").pack(pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.pack()

# Login button
ttk.Button(root, text="Login", command=login).pack(pady=15)

# Sign up button
ttk.Button(root, text="Sign Up", command=sign_up).pack(pady=15)

# Main loop
root.mainloop()
