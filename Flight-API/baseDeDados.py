import sqlite3

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('companhia_aerea.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar tabelas, se não existirem
def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()

# Tabela para passageiros
    cursor.execute('''CREATE TABLE IF NOT EXISTS Passageiros (
                        id INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        sobrenome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefone TEXT,
                        bi TEXT NOT NULL,
                        passaporte TEXT NOT NULL,
                        UNIQUE(email, bi, passaporte)
                    )''')

    # Tabela para voos
    cursor.execute('''CREATE TABLE IF NOT EXISTS Voos (
                        id INTEGER PRIMARY KEY,
                        origem TEXT NOT NULL,
                        destino TEXT NOT NULL,
                        data DATE NOT NULL,
                        hora_partida TIME NOT NULL,
                        hora_prevista_partida TIME NOT NULL,
                        vagas INTEGER NOT NULL,
                        tipo_voo TEXT CHECK( tipo_voo IN ('Voo Direto', 'Voo com Escala', 'Voo Conexão') ) NOT NULL,
                        CONSTRAINT origem_destino_ck CHECK (origem <> destino)
                    )''')

    # Tabela para reservas
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservas (
                        id INTEGER PRIMARY KEY,
                        passageiro_id INTEGER NOT NULL,
                        voo_id INTEGER NOT NULL,
                        data_reserva DATE NOT NULL,
                        FOREIGN KEY (passageiro_id) REFERENCES Passageiros(id),
                        FOREIGN KEY (voo_id) REFERENCES Voos(id),
                        UNIQUE(passageiro_id, voo_id)
                    )''')

    # Tabela para registrar atrasos
    cursor.execute('''CREATE TABLE IF NOT EXISTS Atrasos (
                        id INTEGER PRIMARY KEY,
                        voo_id INTEGER NOT NULL,
                        horas_atraso INTEGER NOT NULL,
                        data_registro DATE NOT NULL,
                        FOREIGN KEY (voo_id) REFERENCES Voos(id)
                    )''')

    conn.commit()
    conn.close()

# Chame a função criar_tabelas para garantir que as tabelas existam
criar_tabelas()
