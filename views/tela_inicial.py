import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TelaInicial(ttk.Frame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.db = db
        self.controller = controller
        self.current_note_id_db = None
        
        # === Variables ===
        self.dark_mode_on = tk.BooleanVar(value=False)
        self.notes_data = []
        self.note_widgets = {}  # Store a dictionary: {note_id_db: (note_frame, label, menu_btn, menu_frame)}

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
        
        self.note_text = tk.Text(self.right_panel, wrap="word", font=("Segoe UI", 11), bd=1, relief="solid", )
        self.note_text.pack(padx=10, pady=10, fill="both", expand=True)

        self.save_button = tk.Button(self.right_panel, text="SAVE", font=("Segoe UI", 10, "bold"), fg="blue", bg="white", command=self.save_note)
        self.save_button.pack(padx=10, pady=5, anchor="se")

        self.add_button = tk.Button(self.left_panel, text="+", font=("Segoe UI", 14, "bold"), fg="green", bg="white", command=self.add_new_note) # Renomeado
        self.add_button.pack(pady=(5, 10), padx=10, fill="x")

        self.refresh_dark_mode()  # Apply initial theme
        self.bind("<Enter>", self._on_tela_inicial_map)


    def _on_tela_inicial_map(self, event = None):
        print("Ta executando")
        if self.db.id_usuario is not None:
            print("Entrou")
            self.unbind("<Enter>")
            self.load_initial_notes()

    def load_initial_notes(self):
        """Carrega todas as notas do banco de dados e cria os widgets."""
        self.notes_data = self.db.get_notes_by_user() 

        for note_id, widgets in list(self.note_widgets.items()): 
            widgets[0].destroy() # Destroi o frame principal da nota
        self.note_widgets.clear()

        for note_info in self.notes_data:
            # Assumindo que note_info é uma tupla (ID, Título, Conteúdo) ou apenas ID
            note_id = note_info[0] if isinstance(note_info, (list, tuple)) else note_info
            initial_content = self.db.get_note_text(note_id) # Pega o conteúdo completo do DB
            self._create_note_widget(note_id, initial_content) # Chamada interna para criar o widget

        if self.notes_data:
            first_note_id = self.notes_data[0][0] if isinstance(self.notes_data[0], (list, tuple)) else self.notes_data[0]
            first_note_widget_info = self.note_widgets.get(first_note_id)
            if first_note_widget_info:
                self.display_note(first_note_widget_info[1], first_note_id) # Passa o label e o ID
            
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

        # itera sobre os valores do dicionário (as tuplas de widgets)
        for note_frame, label, menu_btn, menu_frame in self.note_widgets.values():
            note_frame.configure(bg=bg_panel)
            label.configure(bg=bg_panel, fg=fg_main)
            menu_btn.configure(bg=bg_panel, fg=fg_main)
            menu_frame.configure(bg=bg_panel)
            for child in menu_frame.winfo_children():
                child.configure(bg=bg_panel, fg=fg_main, activebackground=bg_main)

    def toggle_dark_mode(self):
        self.refresh_dark_mode()

    def save_note(self):
        if self.current_note_id_db is None:
            messagebox.showwarning("Aviso", "Nenhuma nota selecionada para salvar.")
            return

        content = self.note_text.get("1.0", tk.END).strip()
        self.db.update_note(self.current_note_id_db, content)
        messagebox.showinfo("Salvo", f"Nota salva com sucesso!")
        
        
        if self.current_note_id_db in self.note_widgets:
            note_frame, label, menu_btn, menu_frame = self.note_widgets[self.current_note_id_db]
            display_content = content.splitlines()[0][:20] + "..." if content else "New Note"
            label.config(text=display_content)


    def display_note(self, clicked_label, note_id):
        self.current_note_id_db = note_id
        txt_tuple = self.db.get_note_text(self.current_note_id_db)
        txt = txt_tuple[0] if txt_tuple else "" # Pega o primeiro elemento da tupla (conteúdo da nota)
        
        self.note_text.delete("1.0", tk.END)
        self.note_text.insert("1.0", txt)

        # mostra a nota selecionada

        for nid, widgets in self.note_widgets.items():
            if nid == note_id:
                widgets[0].config(relief="ridge", bd=2) # borda mais grossa
            else:
                widgets[0].config(relief="solid", bd=1) 


    def add_new_note(self):
        new_note_id = self.db.insert_note() # insere na base de dados e pega o id
        self.notes_data = self.db.get_notes_by_user() # Atualiza a lista de IDs do DB
        
        # Cria e adiciona o widget para a nova nota
        self._create_note_widget(new_note_id, "")
        
        # Exibe a nova nota no painel direito
        new_note_widgets = self.note_widgets.get(new_note_id)
        if new_note_widgets:
            self.display_note(new_note_widgets[1], new_note_id)


    def _create_note_widget(self, note_id, initial_content): # Função interna para criar UM widget de nota
        note_frame = tk.Frame(self.left_panel, bg="white")
        note_frame.pack(fill="x", pady=2, padx=5)

        display_content = initial_content[0] if isinstance(initial_content, tuple) and initial_content else "New Note"
        
        label = tk.Label(note_frame, text=display_content.splitlines()[0][:20] + "..." if display_content else "New Note", bg="white", fg="black", font=("Segoe UI", 11), anchor="w")
        label.pack(side="left", fill="x", expand=True)
        label.bind("<Button-1>", lambda _, lbl=label, nid=note_id: self.display_note(lbl, nid))

        # Create hidden menu frame
        menu_frame = tk.Frame(note_frame, bg="white", relief="raised", bd=1)

        def edit_note_callback():
            menu_frame.pack_forget() # Esconde o menu
            self.display_note(label, note_id) # Exibe a nota no editor

        def delete_note_callback():
            # pergunta pro usuario se ele quer mesmo deletar 
            if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta nota?"):
                self.db.delete_note(note_id)
                
                # remove o widget da interface
                note_frame.destroy()
                
                # Remove a entrada do dicionário de widgets
                if note_id in self.note_widgets:
                    del self.note_widgets[note_id]
                
                # Remove a nota dos dados carregados
                # Para evitar problemas de iteração, recarregue ou remova de notes_data
                self.notes_data = [n_info for n_info in self.notes_data if (n_info[0] if isinstance(n_info, (list, tuple)) else n_info) != note_id]

                # se a nota que foi excluída era a que estava sendo exibida, limpa o text entry
                if self.current_note_id_db == note_id:
                    self.note_text.delete("1.0", tk.END)
                    self.current_note_id_db = None
                
                # se ainda houver notas, seleciona a primeira, senão limpa
                if self.notes_data:
                    first_note_id_after_delete = self.notes_data[0][0] if isinstance(self.notes_data[0], (list, tuple)) else self.notes_data[0]
                    first_note_widget_info = self.note_widgets.get(first_note_id_after_delete)
                    if first_note_widget_info:
                        self.display_note(first_note_widget_info[1], first_note_id_after_delete)
                else:
                    self.note_text.delete("1.0", tk.END)
                    self.current_note_id_db = None


        def toggle_menu():
            if menu_frame.winfo_ismapped():
                menu_frame.pack_forget()
            else:
                # apaga todos os outros menus abertos antes de abrir este
                # print(self.note_widgets.values())
                for widgets_info in self.note_widgets.values():
                    other_menu_frame = widgets_info[3] # (menu_frame) 
                    if other_menu_frame != menu_frame and other_menu_frame.winfo_ismapped():
                        other_menu_frame.pack_forget()
                menu_frame.pack(side="bottom", anchor="e")


        edit_button = tk.Button(menu_frame, text="✏ Edit", command=edit_note_callback, anchor="w")
        edit_button.pack(fill="x", padx=5, pady=(5, 0))

        delete_button = tk.Button(menu_frame, text="🗑 Delete", command=delete_note_callback, anchor="w", bg="red", fg="white")
        delete_button.pack(fill="x", padx=5, pady=(0, 5))


        menu_btn = tk.Button(note_frame, text="⋮", font=("Segoe UI", 10), bg="white", bd=0, command=toggle_menu)
        menu_btn.pack(side="right")

        
        self.note_widgets[note_id] = (note_frame, label, menu_btn, menu_frame)
        self.refresh_dark_mode() 