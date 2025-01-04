from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from geolocalizacao import obter_localizacao_ip  # Importa a função de geolocalização

# Inicialização do banco de dados
db = SQLAlchemy()


# Modelo de usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'

    @property
    def is_active(self):
        return True  # Retorna True para todos os usuários, você pode alterar conforme sua lógica

    def get_id(self):
        return str(self.id)  # Retorna o ID do usuário como string

    @property
    def is_authenticated(self):  # O comportamento padrão é retornar True, indicando que o usuário está autenticado
        return True


# Modelo de caminhoneiro
class Caminhoneiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Caminhoneiro {self.nome}>'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Adiciona para evitar o warning

    # Configuração da chave da API do Google Maps
    app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')  # Armazena a chave em variável de ambiente

    # Inicializa o banco de dados e o login manager
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    # Garante que as tabelas sejam criadas
    with app.app_context():
        db.create_all()

    # Rota da página inicial
    @app.route('/')
    def home():
        return redirect(url_for('login'))  # Redireciona para a página de login

    # Rota de login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            nome_usuario = request.form['username']
            senha = request.form['password']
            usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
            if usuario and usuario.senha == senha:
                login_user(usuario)
                return redirect(url_for('dashboard'))
        return render_template('login.html')

    # Rota de registro
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            nome_usuario = request.form['username']
            senha = request.form['password']
            usuario = Usuario(nome_usuario=nome_usuario, senha=senha)
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    # Rota do Dashboard
    @app.route('/dashboard')
    @login_required
    def dashboard():
        caminhoneiros = Caminhoneiro.query.all()
        google_maps_api_key = "AIzaSyCRBczhYV0C_A4WL_f6a14Dn-wV8KgktBY"  # Defina a chave diretamente aqui
        localizacao = obter_localizacao_ip()  # Chama a função para obter a localização

        if localizacao:
            return render_template(
                'dashboard.html',
                caminhoneiros=caminhoneiros,
                google_maps_api_key=google_maps_api_key,
                localizacao=localizacao
            )

        return render_template('dashboard.html', caminhoneiros=caminhoneiros, google_maps_api_key=google_maps_api_key)

    # Rota para logout
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # Carregar o usuário
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Nova rota para obter a localização do caminhoneiro do usuário logado
    @app.route('/localizacao_usuario')
    @login_required  # Garantir que o usuário esteja logado
    def localizacao_usuario():
        usuario_logado = current_user  # O usuário logado já está acessível através do current_user
        caminhoneiro = Caminhoneiro.query.filter_by(id=usuario_logado.id).first()  # Pega o caminhoneiro correspondente

        if caminhoneiro:
            # Retorna a localização como um JSON
            return jsonify({
                'latitude': caminhoneiro.localizacao.split(',')[0],  # Exemplo: pegar a latitude
                'longitude': caminhoneiro.localizacao.split(',')[1],  # Exemplo: pegar a longitude
                'nome': caminhoneiro.nome
            })
        else:
            return jsonify({'error': 'Caminhoneiro não encontrado'}), 404

    # Rota para obter todas as localizações dos caminhoneiros
    @app.route('/localizacao_caminhoneiros')
    @login_required  # Garante que o usuário esteja logado
    def localizacao_caminhoneiros():
        caminhoneiros = Caminhoneiro.query.all()  # Pega todos os caminhoneiros no banco de dados
        localizacoes = []

        for caminhoneiro in caminhoneiros:
            localizacao = caminhoneiro.localizacao.split(',')
            localizacoes.append({
                'id': caminhoneiro.id,
                'nome': caminhoneiro.nome,
                'latitude': localizacao[0],
                'longitude': localizacao[1]
            })

        return jsonify(localizacoes)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)









