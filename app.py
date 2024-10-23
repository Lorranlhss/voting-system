from getmac import get_mac_address
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'chave_super_secreta'


# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Cria as tabelas ao iniciar o servidor
def create_tables():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS votos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        candidato TEXT NOT NULL,
        mac_address TEXT,
        UNIQUE(username)
    );
    ''')
    conn.close()


# Chamando a função de criação de tabelas na inicialização
with app.app_context():
    create_tables()


# Rota para a página inicial (login)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('votacao'))
        else:
            flash('Login inválido. Verifique seu nome de usuário e senha.')
            return redirect(url_for('login'))

    return render_template('login.html')


# Rota para registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            flash('Registrado com sucesso! Agora você pode fazer login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe.')
            return redirect(url_for('register'))
        finally:
            conn.close()

    return render_template('register.html')


# Rota para a página de votação
@app.route('/votacao', methods=['GET', 'POST'])
def votacao():
    conn = get_db_connection()
    candidatos = [
        {'nome': 'System Ecofire Detector 32'},
        {'nome': 'Garbage Collector Prototype'},
        {'nome': 'Sis-Ama'},
        {'nome': 'Cap. e Arm. Sust. de Água'},
        {'nome': 'Irragação e Contr. de Água'},
        {'nome': 'Ecologicamente Verde'},
        {'nome': 'Gestão do EPI'},
        {'nome': 'EcoMonitor Amazônico'},
        {'nome': 'Oca-Informa'},
        {'nome': 'Rastreador Solar'},
        {'nome': 'Eco MonitorAM'},
        {'nome': 'Fibras Finas'},
        {'nome': 'EcoProcess. D"água '},
        {'nome': 'App-EI'},
        {'nome': 'EcoExtruder'},
        {'nome': 'Suport. Flutuante'},
        {'nome': 'Estiagem Amazônica'},
        {'nome': 'Aqua Logistic'},
        {'nome': 'Puretech'},
        {'nome': 'HydroGen'},
        {'nome': 'Catalix'},
        {'nome': 'Est. de trat. d"água'},
        {'nome': 'Limp. auto. de Igarapé'},
        {'nome': 'Eco - X9'},
        {'nome': 'Energ. Sustentável'},
        {'nome': 'FloraTech'},
        {'nome': 'Fogo Zero'},
        {'nome': 'Plat. de Sust. Amb.'},
        {'nome': 'Water loT'},
        {'nome': 'Monger Iguaçú'},
        {'nome': 'EcoHorta'},
        {'nome': 'Amaz. em Foco: Seg. e M. Amb.'},
        {'nome': 'Spectra'},
        {'nome': 'Solar Med'},
        {'nome': 'EnergyTech'},
        {'nome': 'Amaz. em Chamas'},
        {'nome': 'Faz. Sust. Auto.'},
        {'nome': 'Lamp. Solar Auto.'},
        {'nome': 'Usina Ecológica'},
    ]

    if request.method == 'POST':
        candidato = request.form['candidato']
        username = session['username']

        # Verificar se o usuário já votou
        user_vote = conn.execute(
            'SELECT * FROM votos WHERE username = ?',
            (username,)
        ).fetchone()

        if user_vote:
            flash("Você já votou. Não é permitido votar mais de uma vez.")
            return redirect(url_for('votacao'))

        # Se não votou, insere o voto
        conn.execute(
            'INSERT INTO votos (username, candidato) VALUES (?, ?)',
            (username, candidato)
        )
        conn.commit()

        flash("Voto registrado com sucesso!")
        return redirect(url_for('votacao'))

    return render_template('votacao.html', candidatos=candidatos)


# Rota para retornar os resultados em JSON
@app.route('/resultados-json')
def resultados_json():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT candidato, COUNT(*) as votos
        FROM votos
        GROUP BY candidato
        ORDER BY votos DESC
        LIMIT 5
    """)
    resultados = cursor.fetchall()
    conn.close()

    votos_json = [{'candidato': row['candidato'], 'votos': row['votos']} for row in resultados]
    return jsonify(votos_json)


# Rota para a página de resultados
@app.route('/resultado')
def resultado():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT candidato, COUNT(*) as votos
        FROM votos
        GROUP BY candidato
        ORDER BY votos DESC
        LIMIT 5
    """)
    resultados = cursor.fetchall()
    conn.close()

    return render_template('resultado.html', votos=resultados)


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
