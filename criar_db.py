import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            voto TEXT NOT NULL,
            mac_address TEXT NOT NULL,
            ip_address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabela 'votos' criada com sucesso.")

init_db()