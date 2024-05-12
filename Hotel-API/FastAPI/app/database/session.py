# Função para conectar ao banco de dados
import sqlite3

def conectar_bd():
    conn = sqlite3.connect('app/database/hotel.db')
    return conn