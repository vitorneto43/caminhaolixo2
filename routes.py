from flask import Flask, render_template, request, redirect, url_for
from models import db, Usuario

app = Flask(__name__)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tipo_usuario = request.form['tipo_usuario']  # Obtendo o tipo de usuário

        # Criação do novo usuário
        novo_usuario = Usuario(username=username, password=password, tipo_usuario=tipo_usuario)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('login'))  # Redireciona para a página de login após o cadastro

    return render_template('register.html')  # Retorna o formulário de registro


if __name__ == '__main__':
    app.run(debug=True)

