from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('companhia_aerea.db')
    conn.row_factory = sqlite3.Row
    return conn

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

if __name__ == '__main__':
    app.run(debug=True)
