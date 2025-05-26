import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TelaInicial(ttk.Frame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.db = db
        self.controller = controller

        # === Variables ===
        self.dark_mode_on = tk.BooleanVar(value=False)
        self.note_widgets = []  # Store tuples: (note_frame, label, menu_btn, menu_frame)

        # === Layout ===
        self.columnconfigure(0, weight = 1, minsize = 150)
        self.columnconfigure(1, weight = 3)
        self.rowconfigure(0, weight = 1)

        # === LEFT PANEL WRAPPER ===
        self.left_panel_wrapper = tk.Frame(self)
        self.left_panel_wrapper.grid(row = 0, column = 0, sticky="nsew")

        self.dark_mode_btn = tk.Checkbutton(
            self.left_panel_wrapper,
            text="Dark Mode",
            variable=self.dark_mode_on,
            command=self.toggle_dark_mode,
            bg="white",
            fg="black",
            font=("Segoe UI", 10, "bold"),
            selectcolor="white"
        )
        self.dark_mode_btn.pack(pady=5)

        # === LEFT PANEL ===
        self.left_panel = tk.Frame(self.left_panel_wrapper, bg="white", bd=1, relief="solid")
        self.left_panel.pack(fill="both", expand=True, padx=5, pady=5)

        # === RIGHT PANEL ===
        self.right_panel = tk.Frame(self, bg="white")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5)

        self.note_text = tk.Text(self.right_panel, wrap="word", font=("Segoe UI", 11), bd=1, relief="solid")
        self.note_text.pack(padx=10, pady=10, fill="both", expand=True)

        self.save_button = tk.Button(self.right_panel, text="SAVE", font=("Segoe UI", 10, "bold"), fg="blue", bg="white", command=self.save_note)
        self.save_button.pack(padx=10, pady=5, anchor="se")

        self.add_button = tk.Button(self.left_panel, text="+", font=("Segoe UI", 14, "bold"), fg="green", bg="white", command=self.add_note)
        self.add_button.pack(pady=(5, 10), padx=10, fill="x")

        self.refresh_dark_mode()  # Apply initial theme

    def refresh_dark_mode(self):
        bg_main = "#2e2e2e" if self.dark_mode_on.get() else "white"
        bg_panel = "#3a3a3a" if self.dark_mode_on.get() else "white"
        fg_main = "white" if self.dark_mode_on.get() else "black"
        fg_accent = "lightgreen" if self.dark_mode_on.get() else "green"
        bg_entry = "#444" if self.dark_mode_on.get() else "white"

        self.master.configure(bg=bg_main)
        self.left_panel_wrapper.configure(bg=bg_main)
        self.left_panel.configure(bg=bg_panel)
        self.right_panel.configure(bg=bg_main)
        self.note_text.configure(bg=bg_entry, fg=fg_main, insertbackground=fg_main)
        self.add_button.configure(bg=bg_panel, fg=fg_accent)
        self.save_button.configure(bg=bg_panel, fg="skyblue" if self.dark_mode_on.get() else "blue")
        self.dark_mode_btn.configure(bg=bg_main, fg=fg_main, selectcolor=bg_main)

        for note_frame, label, menu_btn, menu_frame in self.note_widgets:
            note_frame.configure(bg=bg_panel)
            label.configure(bg=bg_panel, fg=fg_main)
            menu_btn.configure(bg=bg_panel, fg=fg_main)
            menu_frame.configure(bg=bg_panel)
            for child in menu_frame.winfo_children():
                child.configure(bg=bg_panel, fg=fg_main, activebackground=bg_main)

    def toggle_dark_mode(self):
        self.refresh_dark_mode()

    def save_note(self):
        content = self.note_text.get("1.0", tk.END).strip()
        messagebox.showinfo("Saved", f"Note content:\n{content[:50]}...")

    def add_note(self):
        note_frame = tk.Frame(self.left_panel, bg="white")
        note_frame.pack(fill="x", pady=2, padx=5)

        label = tk.Label(note_frame, text="New Note", bg="white", fg="black", font=("Segoe UI", 11), anchor="w")
        label.pack(side="left", fill="x", expand=True)
        label.bind("<Button-1>", lambda _: print("Note clicked"))  # Placeholder for note click action

        menu_btn = tk.Button(note_frame, text="⋮", font=("Segoe UI", 10), bg="white", bd=0)
        menu_btn.pack(side="right")

        menu_frame = tk.Frame(note_frame, bg="white", relief="raised", bd=1)

        def edit_note():
            print("Edit clicked")
            menu_frame.place_forget()

        def delete_note():
            note_frame.destroy()
            self.note_widgets.remove((note_frame, label, menu_btn, menu_frame))

        edit_button = tk.Button(menu_frame, text="Edit", command=edit_note, anchor="w")
        edit_button.pack(fill="x")
        delete_button = tk.Button(menu_frame, text="Delete", bg="red", command=delete_note, anchor="w")
        delete_button.pack(fill="x", padx=10)

        def toggle_menu():
            if menu_frame.winfo_ismapped():
                menu_frame.place_forget()
            else:
                menu_frame.place(x=130, y=0)

        menu_btn.configure(command=toggle_menu)

        self.note_widgets.append((note_frame, label, menu_btn, menu_frame))
        self.refresh_dark_mode()  # Update theme when new note is added
