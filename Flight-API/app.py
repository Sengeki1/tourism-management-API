from flask import Flask, render_template, request, jsonify
import sqlite3
import baseDeDados as BD  # Importe o módulo baseDeDados.py

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('companhia_aerea.db')
    conn.row_factory = sqlite3.Row
    return conn

# Chame a função de criação de tabelas de baseDeDados.py para garantir que as tabelas sejam criadas antes de acessá-las
BD.criar_tabelas()

@app.route('/adicionar_passageiro', methods=['POST'])
def adicionar_passageiro():
    data = request.json

    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    email = data.get('email')
    telefone = data.get('telefone')

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Passageiros (nome, sobrenome, email, telefone)
        VALUES (?, ?, ?, ?)
    ''', (nome, sobrenome, email, telefone))
    conn.commit()
    conn.close()

    return jsonify({'message': "Reserva feita com sucesso!"}), 200

# Rotas para listar passageiros e voos disponíveis
@app.route('/listar_passageiros', methods=['GET'])
def listar_passageiros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Passageiros''')
    rows = cursor.fetchall()
    
    passageiros = [dict(row) for row in rows]

    conn.close()
    return jsonify(passageiros)

@app.route('/listar_voos_disponiveis', methods=['GET'])
def listar_voos_disponiveis():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Voos WHERE vagas > 0''')
    rows = cursor.fetchall()

    voos = [dict(row) for row in rows]

    conn.close()
    return jsonify(voos)

if __name__ == '__main__':
    app.run(debug=True)
