from database import db

class Vacina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade_recomendada = db.Column(db.String(50), nullable=False)
    doses = db.Column(db.Integer, nullable=False)
    rede_disponivel = db.Column(db.String(50), nullable=False)
    doenca_prevenida = db.Column(db.String(100), nullable=False)
