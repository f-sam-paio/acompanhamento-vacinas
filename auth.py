from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import Usuario

auth_bp = Blueprint('auth', __name__)

# Rota de registro de usuários
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'usuario_id' in session:
        return redirect('/painel')

    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip().lower()
        senha = request.form['senha']

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('auth.registro'))

        novo_usuario = Usuario(nome=nome, email=email, is_admin=False)
        novo_usuario.set_senha(senha)

        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# Rota de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect('/painel')

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            session['usuario_id'] = usuario.id
            session['is_admin'] = usuario.is_admin
            flash('Login realizado com sucesso!', 'success')
            return redirect('/painel')
        else:
            flash('E-mail ou senha inválidos.', 'danger')

    return render_template('login.html')


# Rota de logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))


