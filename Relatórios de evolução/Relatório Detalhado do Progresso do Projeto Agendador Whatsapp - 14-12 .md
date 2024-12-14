**Relatório Detalhado do Progresso do Projeto Agendador Whatsapp – 14/12**

-----
**Objetivo do Projeto**

Criar uma aplicação Flask para gerenciamento de agendamentos via WhatsApp, incluindo funcionalidades administrativas para cadastro de usuários, agendamentos e envio de notificações.

-----
**Etapas Concluídas**

**1. Estrutura do Projeto**

Criamos e configuramos a estrutura básica do projeto com as seguintes pastas e arquivos:

Projeto\_Agendamento\_Whatsapp/

├── app/

│   ├── \_\_init\_\_.py

│   ├── config/

│   │   ├── \_\_init\_\_.py

│   │   ├── development.py

│   ├── extensions.py

│   ├── models/

│   │   ├── \_\_init\_\_.py

│   │   ├── user.py

│   │   ├── appointment.py

│   ├── routes/

│   │   ├── \_\_init\_\_.py

│   │   ├── main.py

│   │   ├── appointments.py

├── migrations/

├── requirements.txt

├── run.py

- **app/\_\_init\_\_.py**: Configuramos a função create\_app() para inicializar o Flask e registrar extensões e rotas.
- **app/config/development.py**: Definimos as configurações de desenvolvimento, incluindo a URL do banco de dados MySQL.
- **app/extensions.py**: Configuramos o SQLAlchemy e o Flask-Migrate.
-----
**2. Banco de Dados**

1. **Modelos Criados:**
   1. **User** (app/models/user.py):
   1. from app.extensions import db

   1. class User(db.Model):
   1. `    `\_\_tablename\_\_ = "users"

   1. `    `id = db.Column(db.Integer, primary\_key=True)
   1. `    `name = db.Column(db.String(100), nullable=False)
   1. `    `phone = db.Column(db.String(15), unique=True, nullable=False)
   1. `    `created\_at = db.Column(db.DateTime, default=db.func.now())

   1. `    `def \_\_repr\_\_(self):

      `        `return f"<User {self.name}>"

   1. **Appointment** (app/models/appointment.py):
   1. from app.extensions import db
   1. from sqlalchemy.orm import relationship

   1. class Appointment(db.Model):
   1. `    `\_\_tablename\_\_ = "appointments"

   1. `    `id = db.Column(db.Integer, primary\_key=True)
   1. `    `user\_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   1. `    `date = db.Column(db.DateTime, nullable=False)
   1. `    `type = db.Column(db.String(50), nullable=False)
   1. `    `duration = db.Column(db.Integer, nullable=False)
   1. `    `created\_at = db.Column(db.DateTime, default=db.func.now())

   1. `    `user = relationship("User", backref="appointments")

   1. `    `def \_\_repr\_\_(self):

      `        `return f"<Appointment {self.type} on {self.date}>"

1. **Migrações Aplicadas:**
   1. Inicializamos as migrações com o Flask-Migrate:
   1. flask db init
   1. flask db migrate -m "Initial migration"

      flask db upgrade

   1. Verificamos que as tabelas users, appointments e alembic\_version foram criadas corretamente no MySQL.
1. **Timeout do MySQL:**
   1. Ajustamos a configuração para evitar problemas de timeout:
      1. Configuramos o pool do SQLAlchemy no arquivo development.py:
      1. SQLALCHEMY\_ENGINE\_OPTIONS = {
      1. `    `"pool\_pre\_ping": True,
      1. `    `"pool\_recycle": 280,
      1. `    `"pool\_size": 10,
      1. `    `"max\_overflow": 5,

         }

-----
**3. Rotas Implementadas**

1. **Rotas de Usuários** (app/routes/main.py):
   1. **GET /users**: Lista todos os usuários cadastrados.
   1. @main.route("/users", methods=["GET"])
   1. def get\_users():
   1. `    `try:
   1. `        `users = User.query.all()
   1. `        `return jsonify([
   1. `            `{"id": user.id, "name": user.name, "phone": user.phone} for user in users
   1. `        `])
   1. `    `except OperationalError as e:

      `        `return jsonify({"error": "Database connection issue", "details": str(e)}), 500

   1. **POST /users**: Cria um novo usuário no banco de dados.
   1. @main.route("/users", methods=["POST"])
   1. def create\_user():
   1. `    `try:
   1. `        `data = request.json
   1. `        `if not data.get("name") or not data.get("phone"):
   1. `            `return jsonify({"error": "Name and phone are required"}), 400

   1. `        `new\_user = User(name=data["name"], phone=data["phone"])
   1. `        `db.session.add(new\_user)
   1. `        `db.session.commit()

   1. `        `return jsonify({"message": "User created", "id": new\_user.id}), 201
   1. `    `except OperationalError as e:
   1. `        `db.session.rollback()
   1. `        `return jsonify({"error": "Database connection issue", "details": str(e)}), 500
   1. `    `except Exception as e:
   1. `        `db.session.rollback()

      `        `return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

1. **Testes no Postman:**
   1. **GET /users**:
      1. Retornou a lista de usuários corretamente.
      1. Respostas esperadas:
         1. Com usuários: [{"id": 1, "name": "João", "phone": "11999999999"}]
         1. Sem usuários: []
   1. **POST /users**:
      1. Criou novos usuários com sucesso.
      1. Retorno esperado:
      1. {
      1. `    `"message": "User created",
      1. `    `"id": 1

         }

-----
**Onde Paramos**

- Concluímos os endpoints para **usuários** e testamos no Postman com sucesso.
- Verificamos que o banco de dados está funcionando corretamente e que os ajustes de timeout no MySQL estão aplicados.
-----
**Próximos Passos**

1. **Implementar Rotas de Agendamentos:**
   1. Criar os endpoints para GET /appointments e POST /appointments.
   1. Testar no Postman:
      1. Listagem de agendamentos.
      1. Criação de agendamentos vinculados a usuários existentes.
1. **Iniciar Integração com WhatsApp:**
   1. Decidir qual API de terceiros usar (ex.: Twilio, WhatsApp Cloud API).
   1. Configurar as credenciais e iniciar a implementação do envio de notificações.
1. **Melhorar o Tratamento de Erros:**
   1. Garantir que todos os endpoints lidam corretamente com erros inesperados.

Se precisar de qualquer ajuste ou detalhamento adicional, é só avisar! 🚀

