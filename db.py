import sqlite3
from datetime import *

class DB():
    def __init__(self):
        print("Database started")

        self.id_usuario = None

        self.conn = sqlite3.connect('notas.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("PRAGMA foreign_keys = ON;") # ligando as FK's

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL CHECK (LENGTH(senha) > 6)
            );
        """)

        self.conn.commit()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
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
                conteudo TEXT,
                    FOREIGN KEY (id_usuario)
                        REFERENCES Usuario(id_usuario)
                    );
        """)

        self.conn.commit()


# funções CRUD

    def insert_note(self, txt: str) -> None:

        """
        Insere uma nova nota na base de dados. \n\n
        txt: Texto da nota
        """

        self.cursor.execute(""" INSERT INTO Notas (id_usuario, conteudo) VALUES (?, ?) """, (self.id_usuario, txt))
        
        self.conn.commit()
        
    
    def update_note(self, id_nota: int, txt: str) -> None:

        """
        Atualiza a nota do id informado com o valor txt.\n\n
        id_nota: ID da nota que deseja atualizar \n
        txt: Conteúdo que irá ser colocado no valor da nota
        """

        self.cursor.execute("""UPDATE Notas SET conteudo = ? WHERE id_nota = ?""", txt, id_nota)
        self.conn.commit()

    def delete_note(self, id_nota: int) -> None:
        
        """
        Exclue a nota com o id informado.\n\n
        id_nota: ID da nota que deseja excluir
        """
        
        self.cursor.execute("""DELETE FROM Notas WHERE id_nota = ? """, id_nota)
        self.conn.commit()

    
    def get_note_text(self, id_nota: int) -> str:

        """
        Retorna o conteúdo da nota com o id informado.\n\n
        id_nota: ID da nota que deseja ler
        """

        self.cursor.execute("SELECT conteudo FROM Notas WHERE id_nota = ?", id_nota)
        conteudo = "".join(self.cursor.fetchall())
        return conteudo
        

    def sign_user(self, username: str, password: str):

        """Cadastra novo usuário na base de dados e retorna uma exceção se o usuário existir na base de dados"""

        try:
            self.cursor.execute("""INSERT INTO Usuarios (nome, senha) VALUES (?, ?)""", (username, password))
            self.conn.commit()

            self.cursor.execute("""SELECT id_usuario FROM Usuarios WHERE nome = ?""", username)
            self.conn.commit()
            self.id_usuario = self.cursor.fetchone()[0]

        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError("Já existe um usuário com esse nome. ")
        

    def login_user(self, username: str, password: str) -> Exception | None:

        """
        Valida o login do usuário e retorna uma exceção se o usuário não estiver cadastrado na base. \n\n
        username: nome de usuário\n
        password: senha do usuário
        """

        self.cursor.execute("""SELECT nome, senha FROM Usuarios WHERE nome = ?""", (username, ))
        self.conn.commit()

        userdata = self.cursor.fetchone()
        if userdata: 
            if userdata[1] == password:
                self.id_usuario = username
            else:
                raise Exception("Usuário não cadastrado na base de dados!")
        else:
            raise Exception("Usuário não cadastrado na base de dados!")                    
        

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
            self.cursor.execute("""INSERT INTO Logs (id_usuario, acao, data, hora, id_nota) VALUES (?, ?, ?, ?, ?)""", (self.id_usuario, acao, date, timestamp, id_nota, ))
        else:
            self.cursor.execute("""INSERT INTO Logs (id_usuario, acao, data, hora) VALUES (?, ?, ?, ?)""", (self.id_usuario, acao, date, timestamp, ))
        
        self.conn.commit()