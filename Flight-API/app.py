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

# Resto do código do app.py
# Rotas para listar passageiros e voos disponíveis
@app.route('/listar_passageiros')
def listar_passageiros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Passageiros''')
    passageiros = cursor.fetchall()
    conn.close()
    return render_template('passageiros.html', passageiros=passageiros)

@app.route('/listar_voos_disponiveis')
def listar_voos_disponiveis():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Voos WHERE vagas > 0''')
    voos = cursor.fetchall()
    conn.close()
    return render_template('voos_disponiveis.html', voos=voos)

if __name__ == '__main__':
    app.run(debug=True)
