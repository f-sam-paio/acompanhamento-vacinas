class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:senha@localhost/vacinas_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'
