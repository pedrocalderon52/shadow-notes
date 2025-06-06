import sqlite3
from datetime import *

class DB():
    def __init__(self):
        self.id_usuario = None

        self.conn = sqlite3.connect('notas.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("PRAGMA foreign_keys = ON;") # ligando as FK's

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL CHECK (LENGTH(senha) > 6)
            );
        """)

        self.conn.commit()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Logs (
                id_log INTEGER PRIMARY KEY AUTOINCREMENT,
                id_nota INTEGER,
                id_usuario INTEGER NOT NULL,
                acao TEXT NOT NULL,
                data TEXT NOT NULL,
                hora TEXT NOT NULL,
                    
                FOREIGN KEY (id_nota) 
                    REFERENCES Notas(id_nota),
                FOREIGN KEY (id_usuario)
                    REFERENCES Usuarios(id_usuario)
                    );
        """)

        self.conn.commit()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Notas (
                id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                conteudo TEXT DEFAULT '',
                    FOREIGN KEY (id_usuario)
                        REFERENCES Usuarios(id_usuario)
                    );
        """)

        self.conn.commit()


# funções CRUD

    def insert_note(self) -> None:

        """
        Insere uma nova nota na base de dados. \n\n
        txt: Texto da nota
        """
        self.cursor.execute(""" INSERT INTO Notas (id_usuario) VALUES (?) """, (self.id_usuario, ))
        self.conn.commit()
        self.cursor.execute("SELECT id_nota FROM Notas WHERE id_usuario = ?", (self.id_usuario, ))
        return self.cursor.fetchall()[-1]
    
    def update_note(self, id_nota: int, txt: str) -> None:

        """
        Atualiza a nota do id informado com o valor txt.\n\n
        id_nota: ID da nota que deseja atualizar \n
        txt: Conteúdo que irá ser colocado no valor da nota
        """
        if isinstance(id_nota, tuple):
            id_nota = id_nota[0]
        self.cursor.execute("""UPDATE Notas SET conteudo = ? WHERE id_nota = ?""", (txt, id_nota))
        self.conn.commit()

    def delete_note(self, id_nota: int) -> None:
        
        """
        Exclue a nota com o id informado.\n\n
        id_nota: ID da nota que deseja excluir
        """
        if isinstance(id_nota, tuple):
            id_nota = id_nota[0]

        self.cursor.execute("""DELETE FROM Notas WHERE id_nota = ?""", (id_nota, ))
        self.conn.commit()

    
    def get_note_text(self, id_nota: int) -> str:
        if isinstance(id_nota, tuple):
            id_nota = id_nota[0]
        
        self.cursor.execute("SELECT conteudo FROM Notas WHERE id_nota = ?", (id_nota, ))
        conteudo = self.cursor.fetchone()
        return conteudo if conteudo else "" 


    def get_notes_by_user(self):
        self.cursor.execute("""SELECT id_nota FROM Notas WHERE id_usuario = ?""", (self.id_usuario, ))
        notas = self.cursor.fetchall()
        
        notas = list(map(lambda n: n[0], notas))
        return notas
        

    def sign_user(self, username: str, password: str):

        """Cadastra novo usuário na base de dados e retorna uma exceção se o usuário existir na base de dados"""

        try:
            self.cursor.execute("""INSERT INTO Usuarios (nome, senha) VALUES (?, ?)""", (username, password))
            self.conn.commit()

            self.cursor.execute("""SELECT id_usuario FROM Usuarios WHERE nome = ?""", (username, ))  
            self.conn.commit()
            self.id_usuario = self.cursor.fetchone()[0]

        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError("Já existe um usuário com esse nome. ")
        
        self.insert_log("cadastro de usuário")

    def login_user(self, username: str, password: str) -> Exception | None:

        """
        Valida o login do usuário e retorna uma exceção se o usuário não estiver cadastrado na base. \n\n
        username: nome de usuário\n
        password: senha do usuário
        """

        self.cursor.execute("""SELECT nome, senha, id_usuario FROM Usuarios WHERE nome = ?""", (username, ))
        self.conn.commit()

        userdata = self.cursor.fetchone()
        if userdata: 
            if userdata[1] == password:
                self.id_usuario = userdata[2]
            else:
                raise Exception("Usuário não cadastrado na base de dados!")
        else:
            raise Exception("Usuário não cadastrado na base de dados!")   

        self.insert_log("login")                 
        

    def insert_log(self, acao: str, id_nota: int | None = None) -> None:
        """
        Insere um log na base de dados. \n\n
        acao: descrição do log\n
        id_nota (opcional): ID da nota que faz parte da interação

        """


        dt = datetime.now() # pega a data do momento do log e formata-a
        date = dt.strftime("%Y-%m-%d")
        timestamp = dt.strftime("%H:%M:%S")

        if id_nota:
            self.cursor.execute("""INSERT INTO Logs (id_usuario, acao, data, hora, id_nota) VALUES (?, ?, ?, ?, ?);""", (self.id_usuario, acao, date, timestamp, id_nota, ))
        else:
            self.cursor.execute("""INSERT INTO Logs (id_usuario, acao, data, hora) VALUES (?, ?, ?, ?);""", (self.id_usuario, acao, date, timestamp, )) # erro nessa linha 
        
        self.conn.commit()
