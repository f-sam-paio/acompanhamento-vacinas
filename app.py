from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from database import db
from models import VacinaCrianca, VacinaAdolescente, Crianca, Usuario, VacinaAplicada
from auth import auth_bp  # Importando o Blueprint de autenticação
from datetime import datetime, date

# Configuração do aplicativo Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Registro do Blueprint de autenticação
app.register_blueprint(auth_bp)  # Usa rotas diretas como /login e /registro

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
        return redirect(url_for('auth.login'))  # Redireciona para o login se o usuário não estiver logado

    usuario = Usuario.query.get_or_404(session['usuario_id'])

    # Se for admin, pega todos os usuários
    if usuario.is_admin:
        usuarios = Usuario.query.all()
        criancas = []  # Admin não visualiza as crianças neste painel
    else:
        usuarios = []  # Usuário comum não vê todos os usuários
        criancas = Crianca.query.filter_by(usuario_id=usuario.id).all()

    return render_template(
        'painel.html',
        usuario=usuario,
        usuarios=usuarios,
        criancas=criancas
    )

from flask import flash, redirect, url_for

# rota para exclusão de usuário
@app.route('/excluir_usuario/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('painel'))  # Redireciona para o painel após a exclusão

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

#Rota para listar crianças/adolescentes
@app.route('/criancas', methods=['GET'])
def listar_criancas():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    criancas = Crianca.query.filter_by(usuario_id=session['usuario_id']).all()
    return render_template('listar_crianca.html', criancas=criancas)

#Rota para editar crianças/adolescentes
@app.route('/criancas/editar/<int:id>', methods=['GET', 'POST'])
def editar_crianca(id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    crianca = Crianca.query.get_or_404(id)

    # Confere se a criança pertence ao usuário logado
    if crianca.usuario_id != session['usuario_id']:
        flash('Você não tem permissão para editar esta criança.', 'danger')
        return redirect(url_for('listar_criancas'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nascimento_str = request.form.get('data_nascimento')

        if not nome or not data_nascimento_str:
            flash('Preencha todos os campos.', 'danger')
            return redirect(url_for('editar_crianca', id=id))

        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d')
        except ValueError:
            flash('Data de nascimento inválida.', 'danger')
            return redirect(url_for('editar_crianca', id=id))

        crianca.nome = nome
        crianca.data_nascimento = data_nascimento
        db.session.commit()
        flash('Dados da criança atualizados com sucesso!', 'success')
        return redirect(url_for('listar_criancas'))

    return render_template('editar_crianca.html', crianca=crianca)

#Rota para excluir crianças/adolescentes
@app.route('/criancas/excluir/<int:id>', methods=['POST'])
def excluir_crianca(id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    crianca = Crianca.query.get_or_404(id)

    if crianca.usuario_id != session['usuario_id']:
        flash('Você não tem permissão para excluir esta criança.', 'danger')
        return redirect(url_for('listar_criancas'))

    db.session.delete(crianca)
    db.session.commit()
    flash('Criança excluída com sucesso.', 'success')
    return redirect(url_for('listar_criancas'))

def calcular_idade_em_meses(data_nascimento):
    hoje = date.today()
    anos = hoje.year - data_nascimento.year
    meses = hoje.month - data_nascimento.month
    if hoje.day < data_nascimento.day:
        meses -= 1
    return anos * 12 + meses

@app.route('/criancas/<int:crianca_id>/vacinas', methods=['GET', 'POST'])
def gerenciar_vacinas(crianca_id):
    crianca = Crianca.query.get_or_404(crianca_id)
    idade_em_meses = calcular_idade_em_meses(crianca.data_nascimento)

    # Decide se a faixa etária é criança ou adolescente
    if idade_em_meses < 132:  # Criança (0-10 anos + 11 meses) 132 meses = 11 anos
        vacinas = VacinaCrianca.query.all()
        vacina_field = 'vacina_crianca_id'
    else:
        vacinas = VacinaAdolescente.query.all()   
        vacina_field = 'vacina_adolescente_id'

    if request.method == 'POST':
        # Limpa as vacinas aplicadas atuais para esta criança (evita duplicidade)
        VacinaAplicada.query.filter_by(crianca_id=crianca.id).delete()

        # Recebe lista de vacinas marcadas
        vacinas_marcadas = request.form.getlist('vacinas')
        for vacina_id in vacinas_marcadas:
            nova_aplicacao = VacinaAplicada(
                crianca_id=crianca.id,
                aplicada=True
            )
            # Preenche o campo correto
            if vacina_field == 'vacina_crianca_id':
                nova_aplicacao.vacina_crianca_id = int(vacina_id)
            else:
                nova_aplicacao.vacina_adolescente_id = int(vacina_id)

            db.session.add(nova_aplicacao)

        db.session.commit()
        flash('Vacinas atualizadas com sucesso!', 'success')
        return redirect(url_for('painel'))

    # Busca as vacinas aplicadas existentes para marcar os checkboxes
    vacinas_aplicadas = VacinaAplicada.query.filter_by(crianca_id=crianca.id).all()
    vacinas_aplicadas_ids = set()

    for va in vacinas_aplicadas:
        if va.vacina_crianca_id:
            vacinas_aplicadas_ids.add(va.vacina_crianca_id)
        if va.vacina_adolescente_id:
            vacinas_aplicadas_ids.add(va.vacina_adolescente_id)

    return render_template(
        'gerenciar_vacinas.html',
        crianca=crianca,
        vacinas=vacinas,
        vacinas_aplicadas_ids=vacinas_aplicadas_ids,
        idade_em_meses=idade_em_meses
    )

# Rota para Cadastro de vacina (Admin)
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

# Rota para editar vacina (Admin)
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

# Rota para excluir vacina (Admin)
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)