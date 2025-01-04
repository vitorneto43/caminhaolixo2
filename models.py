from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Caminhoneiro  # Importando os modelos


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)

    @staticmethod
    def create_user(username, password, tipo_usuario):
        user = Usuario(username=username, password=password, tipo_usuario=tipo_usuario)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def find_by_username(username):
        return Usuario.query.filter_by(username=username).first()


class Caminhoneiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    placa_veiculo = db.Column(db.String(20), nullable=False)
    tipo_veiculo = db.Column(db.String(50), nullable=False)



app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Exemplo de URI para SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'  # Defina uma chave secreta para Flask-Login

# Inicializando o banco de dados
db.init_app(app)

# Criação das tabelas (deve ser feito uma única vez)
with app.app_context():
    db.create_all()  # Cria todas as tabelas no banco de dados


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tipo_usuario = request.form['tipo_usuario']  # Tipo de usuário (ex: "caminhoneiro" ou "administrador")

        # Criando um novo usuário
        Usuario.create_user(username=username, password=password, tipo_usuario=tipo_usuario)

        return redirect(url_for('login'))  # Redireciona para a página de login após o cadastro

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.find_by_username(username)

        if usuario and usuario.password == password:  # Verifique a senha aqui (idealmente, use hash de senha)
            return redirect(url_for('dashboard'))  # Redireciona para o painel após o login

        return "Login falhou, tente novamente."

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return "Bem-vindo ao painel!"


if __name__ == '__main__':
    app.run(debug=True)


def db():
    return None