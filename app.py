from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import uuid
import socket

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para inicializar o banco de dados
def init_db():
    conn = get_db_connection()
    print("Inicializando o banco de dados e criando a tabela 'votos', se necessário.")
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
    print("Banco de dados inicializado com sucesso.")

# Função para obter o endereço MAC do dispositivo
def get_mac():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                    for elements in range(0, 2*6, 8)][::-1])
    return mac

# Função para obter o endereço IP
def get_ip():
    return socket.gethostbyname(socket.gethostname())

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validando o login
        if username == 'usuario' and password == 'senha':
            session['username'] = username
            return redirect(url_for('votacao'))
        else:
            flash('Credenciais inválidas')
    return render_template('login.html')

@app.route('/votacao', methods=['GET', 'POST'])
def votacao():
    if 'username' not in session:
        return redirect(url_for('login'))

    mac_address = get_mac()
    ip_address = get_ip()

    conn = get_db_connection()
    voto_existente = conn.execute(
        'SELECT * FROM votos WHERE mac_address = ? OR ip_address = ?',
        (mac_address, ip_address)
    ).fetchone()

    if voto_existente:
        flash('Você já votou com este dispositivo.')
        return redirect(url_for('resultado'))

    if request.method == 'POST':
        voto = request.form.get('voto')
        if not voto:
            flash('Por favor, selecione um candidato antes de votar.')
        else:
            conn.execute(
                'INSERT INTO votos (username, voto, mac_address, ip_address) VALUES (?, ?, ?, ?)',
                (session['username'], voto, mac_address, ip_address)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('resultado'))
    
    return render_template('votacao.html')

@app.route('/resultado')
def resultado():
    conn = get_db_connection()
    votos = conn.execute('SELECT voto, COUNT(voto) as count FROM votos GROUP BY voto').fetchall()
    conn.close()
    return render_template('resultado.html', votos=votos)

if __name__ == '_main_':
    init_db()
    app.run(debug=True)