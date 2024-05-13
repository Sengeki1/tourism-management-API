from app.database.session import conectar_bd


def verificar_tabela_reservas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT,
            email_cliente TEXT,
            telefone_cliente TEXT,
            tipo_quarto TEXT,
            check_in INTEGER,
            check_out INTEGER,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()