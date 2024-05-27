from flask import Flask, render_template, request, jsonify
import sqlite3
import baseDeDados as BD  # Importe o módulo baseDeDados.py
from datetime import datetime
from threading import Lock

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('companhia_aerea.db')
    conn.row_factory = sqlite3.Row
    return conn

# Chamando a função de criação de tabelas de baseDeDados.py para garantir que as tabelas sejam criadas antes de acessá-las
BD.criar_tabelas()

# Lock para gerenciar concorrência
lock = Lock()

# Rota para listar passageiros
@app.route('/listar_passageiros')
def listar_passageiros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Passageiros''')
    passageiros = cursor.fetchall()
    conn.close()
    return render_template('passageiros.html', passageiros=passageiros)

# Rota para listar voos disponíveis
@app.route('/listar_voos_disponiveis')
def listar_voos_disponiveis():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Voos WHERE vagas > 0''')
    voos = cursor.fetchall()
    conn.close()
    return render_template('voos_disponiveis.html', voos=voos)

# Rota para adicionar passageiro (renderiza o formulário)
@app.route('/adicionar_passageiro_form')
def adicionar_passageiro_form():
    return render_template('adicionar_passageiro.html')

# Rota para adicionar passageiro (processa os dados)
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

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Passageiros (nome, sobrenome, email, telefone, bi, passaporte)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, sobrenome, email, telefone, bi, passaporte))
        conn.commit()
        return jsonify({'mensagem': 'Passageiro adicionado com sucesso'}), 200
    except sqlite3.IntegrityError as e:
        return jsonify({'mensagem': f'Erro ao adicionar passageiro: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao adicionar passageiro: {str(e)}'}), 500
    finally:
        conn.close()

# Rota para reservar um voo (renderiza o formulário)
@app.route('/reservar_voo_form')
def reservar_voo_form():
    return render_template('reservar_voo.html')

# Rota para reservar um voo (processa os dados)
@app.route('/reservar_voo', methods=['POST'])
def reservar_voo():
    try:
        data = request.get_json()
        passageiro_id = data.get('passageiro_id')
        voo_id = data.get('voo_id')

        if not passageiro_id or not voo_id:
            return jsonify({'mensagem': 'ID do passageiro e ID do voo são obrigatórios'}), 400

        with lock:
            conn = conectar_bd()
            cursor = conn.cursor()

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
            conn.commit()

            return jsonify({'mensagem': 'Reserva realizada com sucesso'}), 200
    except sqlite3.IntegrityError as e:
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
    voos_reservados = []
    for voo in voos:
        voos_reservados.append({
            'id': voo['id'],
            'origem': voo['origem'],
            'destino': voo['destino'],
            'data': voo['data'],
            'hora_partida': voo['hora_partida']
        })
    return jsonify(voos_reservados)

# Rota para renderizar a página HTML de voos reservados
@app.route('/voos_reservados_pagina')
def voos_reservados_pagina():
    return render_template('voos_reservados.html')

if __name__ == '__main__':
    app.run(debug=True)
