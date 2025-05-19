import sqlite3

class DB():
    def __init__(self):

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
                id_nota INTEGER NOT NULL,
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

        self.conn.close()


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
        
