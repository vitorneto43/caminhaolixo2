from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instância do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados (exemplo com SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy com o app
    db.init_app(app)

    # Importa os modelos e cria as tabelas
    from .models import Usuario

    @app.before_first_request
    def criar_tabelas():
        db.create_all()  # Cria todas as tabelas definidas

    return app
