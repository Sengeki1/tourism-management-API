from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import threading
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('companhia_aerea.db')
    conn.row_factory = sqlite3.Row
    return conn

# Chamando a função de criação de tabelas de baseDeDados.py para garantir que as tabelas sejam criadas antes de acessá-las
import baseDeDados as BD  # Importe o módulo baseDeDados.py
BD.criar_tabelas()

# Lock para gerenciar concorrência
lock = threading.Lock()

# Decorator para verificar o token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        
        if not token:
            return jsonify({'mensagem': 'Token não está presente!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE id = ?", (data['id'],))
            current_user = cursor.fetchone()
        except:
            return jsonify({'mensagem': 'Token é inválido!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Função para adicionar um passageiro dentro de uma transação
def adicionar_passageiro_com_transacao(passageiro_data):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Inicia a transação
        cursor.execute("BEGIN TRANSACTION")

        # Adiciona o passageiro
        cursor.execute('''
            INSERT INTO Passageiros (nome, sobrenome, email, telefone, bi, passaporte)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (passageiro_data['nome'], passageiro_data['sobrenome'], 
              passageiro_data['email'], passageiro_data['telefone'],
              passageiro_data['bi'], passageiro_data['passaporte']))

        # Confirma a transação
        conn.commit()
        print("Passageiro adicionado com sucesso!")
    except sqlite3.Error as e:
        # Desfaz a transação em caso de erro
        conn.rollback()
        print(f"Erro ao adicionar passageiro: {e}")
    finally:
        conn.close()

# Rota para registrar usuário
@app.route('/registrar_form')
def registrar_form():
    return jsonify({'mensagem': 'Formulário de registro disponível'}), 200

# Rota para registrar usuário
@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    username = data['username']
    senha = data['senha']
    hashed_password = generate_password_hash(senha, method='sha256')

    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Usuarios (username, senha) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'mensagem': 'Usuário já existe!'}), 400
    finally:
        conn.close()
    
    return jsonify({'mensagem': 'Usuário registrado com sucesso!'}), 200

# Rota para login
@app.route('/login_form')
def login_form():
    return jsonify({'mensagem': 'Formulário de login disponível'}), 200

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    senha = data['senha']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user['senha'], senha):
        return jsonify({'mensagem': 'Login ou senha incorretos!'}), 401

    token = jwt.encode({'id': user['id'], 'exp': datetime.utcnow() + timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

# Rota para listar passageiros
@app.route('/listar_passageiros')
def listar_passageiros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Passageiros''')
    passageiros = cursor.fetchall()
    conn.close()
    passageiros_list = [dict(passageiro) for passageiro in passageiros]
    return jsonify(passageiros_list), 200

# Rota para listar voos disponíveis
@app.route('/listar_voos_disponiveis')
def listar_voos_disponiveis():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Voos WHERE vagas > 0''')
    voos = cursor.fetchall()
    conn.close()
    voos_list = [dict(voo) for voo in voos]
    return jsonify(voos_list), 200

# Rota para adicionar passageiro
@app.route('/adicionar_passageiro', methods=['POST'])
def adicionar_passageiro():
    try:
        data = request.get_json()
        nome = data.get('nome')
        sobrenome = data.get('sobrenome')
        email = data.get('email')
        telefone = data.get('telefone')
        bi = data.get('bi')
        passaporte = data.get('passaporte')

        if not nome or not sobrenome or not email or not bi or not passaporte:
            return jsonify({'mensagem': 'Nome, sobrenome, email, BI e passaporte são obrigatórios'}), 400

        adicionar_passageiro_com_transacao(data)
        return jsonify({'mensagem': 'Passageiro adicionado com sucesso!'}), 200
    except sqlite3.IntegrityError as e:
        return jsonify({'mensagem': f'Erro ao adicionar passageiro: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao adicionar passageiro: {str(e)}'}), 500

# Rota para reservar um voo (renderiza o formulário)
@app.route('/reservar_voo_form')
def reservar_voo_form():
    return jsonify({'mensagem': 'Formulário de reserva de voo disponível'}), 200

# Rota para reservar um voo (processa os dados)
@app.route('/reservar_voo', methods=['POST'])
@token_required
def reservar_voo(current_user):
    try:
        data = request.get_json()
        passageiro_id = data.get('passageiro_id')
        voo_id = data.get('voo_id')

        if not passageiro_id or not voo_id:
            return jsonify({'mensagem': 'ID do passageiro e ID do voo são obrigatórios'}), 400

        with lock:
            conn = conectar_bd()
            cursor = conn.cursor()

            # Inicia a transação
            cursor.execute("BEGIN TRANSACTION")

            # Verificar se há vagas disponíveis
            cursor.execute('SELECT vagas FROM Voos WHERE id = ?', (voo_id,))
            voo = cursor.fetchone()
            if voo is None:
                return jsonify({'mensagem': 'Voo não encontrado'}), 404

            if voo['vagas'] <= 0:
                return jsonify({'mensagem': 'Não há vagas disponíveis para este voo'}), 400

            # Inserir a reserva
            cursor.execute('''
                INSERT INTO Reservas (passageiro_id, voo_id, data_reserva)
                VALUES (?, ?, ?)
            ''', (passageiro_id, voo_id, datetime.now().date()))

            # Atualizar o número de vagas disponíveis
            cursor.execute('UPDATE Voos SET vagas = vagas - 1 WHERE id = ?', (voo_id,))

            # Confirma a transação
            conn.commit()

            return jsonify({'mensagem': 'Reserva realizada com sucesso'}), 200
    except sqlite3.IntegrityError as e:
        # Desfaz a transação em caso de erro
        conn.rollback()
        return jsonify({'mensagem': f'Erro ao realizar reserva: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao realizar reserva: {str(e)}'}), 500
    finally:
        conn.close()

# Rota para listar voos reservados
@app.route('/voos_reservados')
def voos_reservados():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT Voos.id, Voos.origem, Voos.destino, Voos.data, Voos.hora_partida
                      FROM Voos
                      INNER JOIN Reservas ON Voos.id = Reservas.voo_id''')
    voos = cursor.fetchall()
    conn.close()
    voos_reservados = [dict(voo) for voo in voos]
    return jsonify(voos_reservados), 200

# Rota para renderizar a página HTML de voos reservados
@app.route('/voos_reservados_pagina')
def voos_reservados_pagina():
    return jsonify({'mensagem': 'Página de voos reservados disponível'}), 200

# Rota para listar as reservas do usuário
@app.route('/minhas_reservas', methods=['GET'])
@token_required
def minhas_reservas(current_user):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT R.id, V.origem, V.destino, V.data, V.hora_partida
                      FROM Voos V
                      INNER JOIN Reservas R ON V.id = R.voo_id
                      WHERE R.passageiro_id = ?''', (current_user['id'],))
    reservas = cursor.fetchall()
    conn.close()
    reservas_list = [dict(reserva) for reserva in reservas]
    return jsonify(reservas_list), 200

# Rota para renderizar a página HTML de reservas do usuário
@app.route('/minhas_reservas_pagina')
@token_required
def minhas_reservas_pagina(current_user):
    return jsonify({'mensagem': 'Página de reservas do usuário disponível'}), 200

@app.route("/sistema_pagamento", methods=["POST"])
def sistema_pagamento():
    dados_pagamento = request.get_json()
    valor = dados_pagamento["valor"]
    descricao = dados_pagamento["descricao"]

    # Simula o processamento do pagamento
    if random.random() < 0.9:  # 90% de chance de sucesso
        return jsonify({"mensagem": "Pagamento com sucesso", "valor": valor, "descricao": descricao}), 200
    else:
        return jsonify({"mensagem": "Falha no pagamento"}), 400

if __name__ == '__main__':
    app.run(debug=True)

