import sqlite3

class bancoDeDados:
    def __init__(self):
        self.conection = sqlite3.connect('banco.db')
        self.cursor = self.conection.cursor()

    def criar_tabelas(self):
        self.cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='user';
        """)
        result = self.cursor.fetchone()
        
        if result is None:
            self.cursor.execute("""
            CREATE TABLE user(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50),
                email VARCHAR(50),
                senha VARCHAR(20)
            )
            """)

        self.cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='anime';
        """)
        result = self.cursor.fetchone()
        
        if result is None:
            self.cursor.execute("""
            CREATE TABLE anime(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                id_user INTEGER,
                nome_anime VARCHAR(50),
                temporada VARCHAR(50),
                episodio VARCHAR(20),
                FOREIGN KEY (id_user) REFERENCES user(id)
            )
            """)

    def __str__(self):
        return str(self.conection)
