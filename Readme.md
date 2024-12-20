﻿**Projeto Agendamento WhatsApp**

Este é um projeto local desenvolvido em Python com o framework Flask, projetado para facilitar o agendamento de consultas com diferentes tipos, valores e durações. Ele inclui funcionalidades administrativas, como configuração de horários de trabalho, tipos de consulta e folgas. O projeto segue uma estrutura modular, visando organização e escalabilidade.

**Estrutura de Pastas**

Abaixo está a estrutura organizada e detalhada do projeto:

Projeto\_Agendamento\_Whatsapp/

├── app/

│   ├── \_\_init\_\_.py           # Inicialização do app Flask

│   ├── config/

│   │   ├── \_\_init\_\_.py       # Gerenciamento de configurações

│   │   ├── base\_config.py    # Configuração base (default)

│   │   ├── development.py    # Configurações para desenvolvimento

│   │   ├── production.py     # Configurações para produção

│   │   ├── testing.py        # Configurações para testes

│   ├── extensions.py         # Registro de extensões Flask

│   ├── logging.py            # Configuração de logs

│   ├── controllers/          # Camada de controladores

│   │   ├── \_\_init\_\_.py       # Inicialização dos controladores

│   │   ├── user\_controller.py # Lógica central de usuários

│   │   ├── booking\_controller.py # Lógica central de agendamentos

│   │   ├── admin\_controller.py # Lógica central de administração

│   ├── routes/               # Rotas organizadas com Blueprints

│   │   ├── \_\_init\_\_.py       # Registro central de blueprints

│   │   ├── user\_routes.py    # Rotas de usuários

│   │   ├── admin\_routes.py   # Rotas de administração

│   │   ├── booking\_routes.py # Rotas de agendamentos

│   ├── models/               # Modelos do banco de dados

│   │   ├── \_\_init\_\_.py       # Inicialização dos modelos

│   │   ├── user\_model.py     # Modelo de usuários

│   │   ├── booking\_model.py  # Modelo de agendamentos

│   │   ├── settings\_model.py # Configurações do administrador

│   ├── services/             # Lógica de negócio e serviços

│   │   ├── \_\_init\_\_.py       # Inicialização dos serviços

│   │   ├── user\_service.py   # Lógica de usuários

│   │   ├── booking\_service.py# Lógica de agendamentos

│   │   ├── admin\_service.py  # Lógica de administração

│   ├── repositories/         # Camada de repositório

│   │   ├── \_\_init\_\_.py       # Inicialização dos repositórios

│   │   ├── user\_repository.py # Operações no banco de dados para usuários

│   │   ├── booking\_repository.py # Operações no banco de dados para agendamentos

│   │   ├── admin\_repository.py # Operações no banco de dados para admins

│   ├── templates/            # Templates HTML

│   │   ├── layout.html       # Layout base

│   │   ├── user/             # Páginas relacionadas a usuários

│   │   │   ├── index.html    # Página inicial do usuário

│   │   ├── admin/            # Páginas de administração

│   │   │   ├── dashboard.html# Painel administrativo

│   │   ├── booking/          # Páginas de agendamentos

│   │       ├── form.html     # Formulário de agendamento

│   ├── static/               # Arquivos estáticos

│   │   ├── css/              # Estilos

│   │   ├── js/               # Scripts

│   │   ├── images/           # Imagens

├── api/                      # API modularizada por versões

│   ├── \_\_init\_\_.py           # Inicialização da API

│   ├── v1/                   # Primeira versão da API

│   │   ├── \_\_init\_\_.py       # Registro da API v1

│   │   ├── user\_api.py       # Endpoints de usuários

│   │   ├── booking\_api.py    # Endpoints de agendamentos

├── tests/                    # Testes organizados

│   ├── routes/               # Testes de rotas

│   ├── models/               # Testes de modelos

│   ├── services/             # Testes de serviços

│   ├── repositories/         # Testes de repositórios

│   ├── utils/                # Testes de utilitários

├── migrations/               # Migrações do banco de dados

├── scripts/                  # Scripts de automação

│   ├── init\_db.py            # Script para inicializar o banco

│   ├── backup\_db.py          # Script para backup do banco

│   ├── reset\_db.py           # Script para reinicializar o banco

├── docs/                     # Documentação do projeto

│   ├── api\_docs.md           # Documentação das rotas da API

│   ├── setup\_guide.md        # Guia de configuração

│   ├── project\_structure.md  # Explicação da estrutura do projeto

├── requirements.txt          # Dependências do projeto

├── README.md                 # Documentação principal

├── run.py                    # Arquivo principal para rodar o app

**Funcionalidades**

**Para Usuários:**

- Agendar consultas selecionando tipo, data e horário.
- Visualizar, editar ou cancelar consultas agendadas.

**Para Administradores:**

- Configurar horários de trabalho.
- Definir tipos de consulta, incluindo duração e valor.
- Gerenciar folgas e indisponibilidades.

**Tecnologias Utilizadas**

- **Backend:** Python (Flask)
- **Banco de Dados:** SQLite (padrão, mas substituível por outros sistemas SQL)
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** Flask-RESTful para implementação futura de APIs
- **Testes:** Pytest
- **Logs:** Configuração centralizada para rastreamento de eventos e erros

**Como Executar**

1. Clone o repositório:

   git clone https://github.com/GilmarPiresTech/Projeto\_Agendamento\_Whatsapp.git

1. Navegue até o diretório do projeto:

   cd Projeto\_Agendamento\_Whatsapp

1. Crie e ative um ambiente virtual:
1. python -m venv venv
1. source venv/bin/activate  # Para Linux/macOS

   venv\Scripts\activate   # Para Windows

1. Instale as dependências:

   pip install -r requirements.txt

1. Execute o servidor:

   python run.py

1. Acesse a aplicação em:
   1. **Usuários:** http://localhost:5000/user
   1. **Administração:** http://localhost:5000/admin

**Futuras Expansões**

- Integração com APIs de pagamento.
- Suporte a notificações em tempo real (ex.: Flask-SocketIO).
- Modularização para microserviços.
-----
**Autor:** [GilmarPiresTech](https://github.com/GilmarPiresTech)
**Licença:** MIT

