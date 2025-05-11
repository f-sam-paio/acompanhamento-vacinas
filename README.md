# 💉 Sistema para Acompanhamento de Vacinas

Este projeto é um sistema web para acompanhamento do calendário de vacinação de crianças e adolescentes. Permite o cadastro de responsáveis e dependentes, a visualização das vacinas recomendadas pela Sociedade Brasileira de Imunizações (SBIm), o registro de vacinas aplicadas e o acompanhamento do histórico de vacinação.

---

## 🛠 Tecnologias Utilizadas

- **Backend:** Python 3.x, Flask, Flask-SQLAlchemy  
- **Banco de Dados:** PostgreSQL  
- **Frontend:** Jinja2, HTML5, Bootstrap 5  

---

## 📋 Funcionalidades

- ✅ Cadastro e login de usuários responsáveis (entregue)
- ✅ Exibição do calendário vacinal conforme faixa etária (SBIm) (entregue)
- ✅ Cadastro de crianças e adolescentes (Futuro)
- ✅ Registro de vacinas (Futuro)
- ✅ Visualização do histórico de vacinação (Futuro)
---

## 🧱 Estrutura do Projeto

ACOMPANHAMENTO-VACINAS/
│
├── templates/
│ ├── cadastrar_crianca.html
│ ├── cadastrar_vacina.html
│ ├── editar_crianca.html
│ ├── editar_vacina.html
│ ├── index.html
│ ├── listar_crianca.html
│ ├── listar_vacinas.html
│ ├── listar_vacinas_criancas.html
│ ├── listar_vacinas_adolescentes.html
│ ├── login.html
│ ├── painel.html
│ └── register.html
│
├── .gitignore
├── app.py # Arquivo principal da aplicação Flask
├── auth.py # Rotas e lógica de autenticação
├── config.py # Configurações (inclui string do banco)
├── database.py # Inicialização do SQLAlchemy
├── models.py # Definição das tabelas (Usuário, Criança, Vacina, etc)
├── requirements.txt # Dependências do projeto
└── README.md # Documentação do projeto

---

## ⚙️ Instalação e Execução Local

### Pré-requisitos

- Python 3.10+
- PostgreSQL instalado e rodando
- Git

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/acompanhamento-vacinas.git
cd acompanhamento-vacinas
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados no `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:senha@localhost/vacinas_db'
```

5. Inicialize o banco:
```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

6. Rode a aplicação:
```bash
python app.py
```

Acesse: [http://127.0.0.1:5000]

---

## 👩‍🔬 Sobre o Projeto

Este sistema foi desenvolvido com fins acadêmicos e educativos. O objetivo principal é proporcionar uma ferramenta simples e acessível para acompanhar a vacinação de crianças e adolescentes conforme recomendações da **SBIm**.

---

## 📌 Importante

O código é apenas para fins educacionais ou uso pessoal.

É proibida sua redistribuição para uso comercial.

---

## 🙋‍♀️ Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir _issues_ e _pull requests_.
