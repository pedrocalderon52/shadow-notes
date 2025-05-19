import tkinter as tk
from tkinter import messagebox
import re # It helps to search for patterns in strings

# Dummy credentials (replace this with a database later)
VALID_USERNAME = "bobo"
VALID_PASSWORD = "5270"

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == VALID_USERNAME and password == VALID_PASSWORD: # Change to database logic when ready
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
    else:
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
        messagebox.showinfo("Registration Successful", f"Account created for {username}!")

# Create main window
root = tk.Tk()
root.title("Login Page")
root.geometry("400x300")
root.resizable(False, False)

# Username entry label
tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack()

# Password entry label
tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Login button
tk.Button(root, text="Login", command=login).pack(pady=15)

# Sign up button
tk.Button(root, text="Sign Up", command=sign_up).pack(pady=15)

# Main loop
root.mainloop()
