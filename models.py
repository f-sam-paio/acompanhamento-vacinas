from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from sqlalchemy.dialects.postgresql import ARRAY

# Modelo de Usuário (Admin ou Usuário Comum)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Definindo a chave primária
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Define se é admin

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

# Modelo de Vacinas para Crianças
class VacinaCrianca(db.Model):
    __tablename__ = 'vacina_crianca'
    id = db.Column(db.Integer, primary_key=True)
    nome_vacina = db.Column(db.String(200), nullable=False)
    idade_recomendada = db.Column(db.String(50), nullable=False)
    idades_em_meses = db.Column(ARRAY(db.Integer))  # Novo campo para uso em lógica futura - converte tudo para meses:"12-15 meses" → [12, 13, 14, 15] "5 anos" → [60]
    doses = db.Column(db.Integer, nullable=False)
    rede_disponivel = db.Column(db.String(100), nullable=False)
    doenca_prevenida = db.Column(db.String(200), nullable=False)

# Modelo de Vacinas para Adolescentes
class VacinaAdolescente(db.Model):
    __tablename__ = 'vacina_adolescente'
    id = db.Column(db.Integer, primary_key=True)
    nome_vacina = db.Column(db.String(200), nullable=False)
    idade_recomendada = db.Column(db.String(50), nullable=False)
    idades_em_meses = db.Column(ARRAY(db.Integer))  # Novo campo para uso em lógica futura - converte tudo para meses:"12-15 meses" → [12, 13, 14, 15] "5 anos" → [60]
    doses = db.Column(db.Integer, nullable=False)
    rede_disponivel = db.Column(db.String(100), nullable=False)
    doenca_prevenida = db.Column(db.String(200), nullable=False)

# Modelo para Crianças/Adolescentes cadastrados pelo usuário
class Crianca(db.Model):
    __tablename__ = 'crianca'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('criancas', lazy=True))