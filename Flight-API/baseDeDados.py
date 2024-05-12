import sqlite3
from datetime import datetime, timedelta

# Conexão com o banco de dados (ou criação do banco, se não existir)
conn = sqlite3.connect('companhia_aerea.db')
cursor = conn.cursor()

# Tabela para passageiros
cursor.execute('''CREATE TABLE IF NOT EXISTS Passageiros (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    telefone TEXT
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
                    CONSTRAINT origem_destino_ck CHECK (origem <> destino)
                )''')

# Tabela para reservas
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservas (
                    id INTEGER PRIMARY KEY,
                    passageiro_id INTEGER NOT NULL,
                    voo_id INTEGER NOT NULL,
                    data_reserva DATE NOT NULL,
                    FOREIGN KEY (passageiro_id) REFERENCES Passageiros(id),
                    FOREIGN KEY (voo_id) REFERENCES Voos(id)
                )''')

# Tabela para registrar atrasos
cursor.execute('''CREATE TABLE IF NOT EXISTS Atrasos (
                    id INTEGER PRIMARY KEY,
                    voo_id INTEGER NOT NULL,
                    horas_atraso INTEGER NOT NULL,
                    data_registro DATE NOT NULL,
                    FOREIGN KEY (voo_id) REFERENCES Voos(id)
                )''')

# Função para adicionar um novo passageiro
def adicionar_passageiro(nome, sobrenome, email, telefone=None):
    try:
        cursor.execute('''INSERT INTO Passageiros (nome, sobrenome, email, telefone)
                          VALUES (?, ?, ?, ?)''', (nome, sobrenome, email, telefone))
        conn.commit()
        print("Passageiro adicionado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: E-mail já cadastrado.")

# Função para adicionar um novo voo
def adicionar_voo(origem, destino, data, hora_partida, hora_prevista_partida, vagas):
    cursor.execute('''INSERT INTO Voos (origem, destino, data, hora_partida, hora_prevista_partida, vagas)
                      VALUES (?, ?, ?, ?, ?, ?)''', (origem, destino, data, hora_partida, hora_prevista_partida, vagas))
    conn.commit()
    print("Voo adicionado com sucesso!")

# Função para realizar uma reserva
def realizar_reserva(passageiro_id, voo_id):
    try:
        data_reserva = datetime.now().date()
        cursor.execute('''INSERT INTO Reservas (passageiro_id, voo_id, data_reserva)
                          VALUES (?, ?, ?)''', (passageiro_id, voo_id, data_reserva))
        cursor.execute('''UPDATE Voos SET vagas = vagas - 1 WHERE id = ?''', (voo_id,))
        conn.commit()
        print("Reserva realizada com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Passageiro ou voo não encontrados.")

# Função para listar todos os voos disponíveis
def listar_voos_disponiveis():
    cursor.execute('''SELECT * FROM Voos WHERE vagas > 0''')
    voos = cursor.fetchall()
    if not voos:
        print("Nenhum voo disponível no momento.")
    else:
        print("Voos Disponíveis:")
        for voo in voos:
            print(f"ID: {voo[0]}, Origem: {voo[1]}, Destino: {voo[2]}, Data: {voo[3]}, Hora de Partida: {voo[4]}, Vagas: {voo[5]}")

# Função para cancelar um voo
def cancelar_voo(voo_id):
    try:
        cursor.execute('''DELETE FROM Voos WHERE id = ?''', (voo_id,))
        cursor.execute('''DELETE FROM Reservas WHERE voo_id = ?''', (voo_id,))
        cursor.execute('''DELETE FROM Atrasos WHERE voo_id = ?''', (voo_id,))
        conn.commit()
        print("Voo cancelado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro ao cancelar o voo.")

# Função para registrar um atraso de voo
def registrar_atraso_voo(voo_id, horas_atraso):
    try:
        data_registro = datetime.now().date()
        cursor.execute('''INSERT INTO Atrasos (voo_id, horas_atraso, data_registro)
                          VALUES (?, ?, ?)''', (voo_id, horas_atraso, data_registro))
        cursor.execute('''SELECT hora_prevista_partida FROM Voos WHERE id = ?''', (voo_id,))
        hora_prevista_partida = cursor.fetchone()[0]
        nova_hora_partida = (datetime.strptime(hora_prevista_partida, '%H:%M') + timedelta(hours=horas_atraso)).strftime('%H:%M')
        cursor.execute('''UPDATE Voos SET hora_partida = ? WHERE id = ?''', (nova_hora_partida, voo_id))
        conn.commit()
        print("Atraso registrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro ao registrar o atraso.")

# Lista de países
paises = ['Brasil', 'Estados Unidos', 'França', 'Alemanha', 'Japão', 'China', 'Itália', 'Rússia', 'Austrália', 'Canadá']

# Função para adicionar voos entre países
def adicionar_voos_entre_paises(paises, data_inicio, numero_voos_por_pais):
    for origem in paises:
        for destino in paises:
            if origem != destino:
                for i in range(numero_voos_por_pais):
                    adicionar_voo(origem, destino, data_inicio, f'{i}:00', f'{i}:00', 100)

# Adicionar voos entre países para os próximos 10 dias
data_inicio = '2024-05-01'
numero_voos_por_pais = 3
for _ in range(10):
    adicionar_voos_entre_paises(paises, data_inicio, numero_voos_por_pais)
    data_inicio = (datetime.strptime(data_inicio, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

# Listar voos disponíveis
listar_voos_disponiveis()

# Exemplo de cancelamento de voo
cancelar_voo(1)

# Exemplo de registro de atraso de voo (aumentar a hora de partida em 2 horas)
registrar_atraso_voo(2, 2)

# Fechar conexão com o banco de dados
conn.close()
