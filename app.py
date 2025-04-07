from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from database import db
from models import VacinaCrianca, VacinaAdolescente, Crianca, Usuario
from auth import auth_bp  # Importando o Blueprint de autenticação
from datetime import datetime
from importar_vacinas import importar_bp

# Configuração do aplicativo Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Registro do Blueprint de autenticação
app.register_blueprint(auth_bp)  # Usa rotas diretas como /login e /registro
app.register_blueprint(importar_bp)  # Tabela de vacinas

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para listar vacinas para crianças (0 a 10 anos)
@app.route('/vacinas/criancas')
def listar_vacinas_criancas():
  
    vacinas_criancas = VacinaCrianca.query.all() 

    # Imprime o conteúdo de vacinas_criancas para depuração
    print(vacinas_criancas)

    return render_template('listar_vacinas_criancas.html', vacinas_criancas=vacinas_criancas)

# Rota para listar vacinas para adolescentes (11 a 17 anos)
@app.route('/vacinas/adolescentes')
def listar_vacinas_adolescentes():
    # Removendo o filtro temporariamente para depuração
    vacinas_adolescentes = VacinaAdolescente.query.all()  # Remove o filtro temporariamente

    # Imprime o conteúdo de vacinas_adolescentes para depuração
    print(vacinas_adolescentes)

    return render_template('listar_vacinas_adolescentes.html', vacinas_adolescentes=vacinas_adolescentes)

# Rota para o painel inicial (após login)
@app.route('/painel')
def painel():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.get_or_404(session['usuario_id'])
    criancas = Crianca.query.filter_by(usuario_id=usuario.id).all()

    return render_template('painel.html', usuario=usuario, criancas=criancas)

# Cadastro de criança/adolescente
@app.route('/criancas/cadastrar', methods=['GET', 'POST'])
def cadastrar_crianca():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')

        total = Crianca.query.filter_by(usuario_id=session['usuario_id']).count()
        if total >= 3:
            flash('Você só pode cadastrar até 3 crianças/adolescentes.', 'warning')
            return redirect(url_for('painel'))

        nova_crianca = Crianca(nome=nome, data_nascimento=data_nascimento, usuario_id=session['usuario_id'])
        db.session.add(nova_crianca)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('painel'))

    return render_template('cadastrar_crianca.html')

# Cadastro de vacina (Admin)
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_vacina():
    if request.method == 'POST':
        nome_vacina = request.form['nome_vacina']
        idade_recomendada = request.form['idade_recomendada']
        doses = int(request.form['doses'])
        rede_disponivel = request.form['rede_disponivel']
        doenca_prevenida = request.form['doenca_prevenida']
        tipo = request.form['tipo']

        if tipo == 'crianca':
            nova = VacinaCrianca(
                nome_vacina=nome_vacina,
                idade_recomendada=idade_recomendada,
                doses=doses,
                rede_disponivel=rede_disponivel,
                doenca_prevenida=doenca_prevenida
            )
        else:
            nova = VacinaAdolescente(
                nome_vacina=nome_vacina,
                idade_recomendada=idade_recomendada,
                doses=doses,
                rede_disponivel=rede_disponivel,
                doenca_prevenida=doenca_prevenida
            )

        db.session.add(nova)
        db.session.commit()
        flash('Vacina cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_vacina'))  # Redireciona para cadastrar nova vacina

    return render_template('cadastrar_vacina.html')

# Edição de vacina (Admin)
@app.route('/vacinas/editar/<tipo>/<int:id>', methods=['GET', 'POST'])
def editar_vacina(tipo, id):
    modelo = VacinaCrianca if tipo == 'crianca' else VacinaAdolescente
    vacina = modelo.query.get_or_404(id)

    if request.method == 'POST':
        vacina.nome = request.form['nome_vacina']
        vacina.idade_recomendada = request.form['idade_recomendada']
        vacina.doses = int(request.form['doses'])
        vacina.rede_disponivel = request.form['rede_disponivel']
        vacina.doenca_prevenida = request.form['doenca_prevenida']
        db.session.commit()
        flash('Vacina atualizada com sucesso!', 'success')
        
        # Redireciona de volta para a lista de vacinas para crianças ou adolescentes
        if tipo == 'crianca':
            return redirect(url_for('listar_vacinas_criancas'))
        else:
            return redirect(url_for('listar_vacinas_adolescentes'))

    return render_template('editar_vacina.html', vacina=vacina, tipo=tipo)

# Exclusão de vacina (Admin)
@app.route('/vacinas/excluir/<tipo>/<int:id>', methods=['POST'])
def excluir_vacina(tipo, id):
    modelo = VacinaCrianca if tipo == 'crianca' else VacinaAdolescente
    vacina = modelo.query.get_or_404(id)
    db.session.delete(vacina)
    db.session.commit()
    flash('Vacina excluída com sucesso!', 'success')
    
    # Redireciona de volta para a lista de vacinas para crianças ou adolescentes
    if tipo == 'crianca':
        return redirect(url_for('listar_vacinas_criancas'))
    else:
        return redirect(url_for('listar_vacinas_adolescentes'))

# Proteção para rotas administrativas
@app.before_request
def restringir_acesso_admin():
    rotas_admin = ['cadastrar_vacina', 'editar_vacina', 'excluir_vacina']
    if request.endpoint in rotas_admin:
        if 'usuario_id' not in session or not session.get('is_admin', False):
            return redirect(url_for('auth.login'))

# Criação das tabelas no banco ao iniciar
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)