from flask import Flask, render_template, request, redirect, url_for
from config import Config
from database import db
from models import Vacina

# Configuração do aplicativo Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Rota para exibir a lista de vacinas
@app.route('/vacinas')
def listar_vacinas():
    vacinas = Vacina.query.all()
    return render_template('listar_vacinas.html', vacinas=vacinas)

# Rota para exibir o formulário de cadastro de vacina
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_vacina():
    if request.method == 'POST':
        nome = request.form['nome']
        idade_recomendada = request.form['idade_recomendada']
        doses = int(request.form['doses'])
        rede_disponivel = request.form['rede_disponivel']
        doenca_prevenida = request.form['doenca_prevenida']

        # Cria a nova vacina e insere no banco de dados
        nova_vacina = Vacina(
            nome=nome,
            idade_recomendada=idade_recomendada,
            doses=doses,
            rede_disponivel=rede_disponivel,
            doenca_prevenida=doenca_prevenida
        )
        db.session.add(nova_vacina)
        db.session.commit()

        return redirect(url_for('listar_vacinas'))

    return render_template('cadastrar_vacina.html')

# Rota para editar a vacina
@app.route('/vacinas/editar/<int:id>', methods=['GET', 'POST'])
def editar_vacina(id):
    vacina = Vacina.query.get_or_404(id) # Obtém a vacina ou retorna 404 se não encontrar
    
    if request.method == 'POST':
        vacina.nome = request.form['nome']
        vacina.idade_recomendada = request.form['idade_recomendada']
        vacina.doses = int(request.form['doses'])
        vacina.rede_disponivel = request.form['rede_disponivel']
        vacina.doenca_prevenida = request.form['doenca_prevenida']

        db.session.commit()
        return redirect(url_for('listar_vacinas'))
    
    return render_template('editar_vacina.html', vacina=vacina)

# Rota para excluir a vacina
@app.route('/vacinas/excluir/<int:id>', methods=['POST'])
def excluir_vacina(id):
    vacina = Vacina.query.get_or_404(id)
    db.session.delete(vacina)
    db.session.commit()
    return redirect(url_for('listar_vacinas'))

# Script para criar a tabela e inserir vacinas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
