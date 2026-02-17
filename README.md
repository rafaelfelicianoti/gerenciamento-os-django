# Sistema de Gerenciamento de Ordens de Serviço

Sistema web desenvolvido em Django para controle de clientes, orçamentos e ordens de serviço, permitindo a criação de OS apenas a partir de orçamentos aprovados.

---

## 📌 Funcionalidades

- ✅ Cadastro e gerenciamento de clientes
- ✅ Gerenciamento de usuários com autenticação personalizada (JWT)
- ✅ Criação e gerenciamento de orçamentos com status (aberto, enviado, aprovado)
- ✅ Aprovação de orçamentos
- ✅ Geração de ordens de serviço vinculadas **apenas** a orçamentos aprovados
- ✅ Controle de status das OS (aberto, em_andamento, concluído)
- ✅ Gerenciamento de funcionários com roles (Gerente, Secretária, Operador, Encarregado)
- ✅ Painel administrativo completo com Django Admin
- ✅ API REST com autenticação JWT
- ✅ Testes automatizados

---

## 🚀 Tecnologias

- **Backend:** Python 3.10+, Django 5.2
- **Banco de Dados:** PostgreSQL
- **API:** Django Rest Framework
- **Autenticação:** JWT (djangorestframework_simplejwt)
- **Ferramentas:** Git, pytest, Postgres

---

## ✅ Requisitos

- Python 3.10+
- PostgreSQL 12+
- Git
- pip ou poetry

---

## ▶️ Como executar o projeto

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/rafaelfelicianoti/gerenciamento-os-django.git
cd gerenciamento-os-django
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv venv
```

**No Windows:**
```bash
venv\Scripts\activate
```

**No Linux/Mac:**
```bash
source venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as credenciais do PostgreSQL:

```env
# Banco de Dados
DB_NAME=gerenciamento_os
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
```

### 5️⃣ Execute as migrações

```bash
python manage.py migrate
```

### 6️⃣ Crie um superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções na tela para criar um admin.

### 7️⃣ (Opcional) Popule o banco com dados de teste

```bash
python manage.py shell
```

Dentro do shell, execute:
```python
exec(open('populate_data.py').read())
```

Isso criará dados realísticos de exemplo (clientes, funcionários, orçamentos e OS).

### 8️⃣ Inicie o servidor

```bash
python manage.py runserver
```

### 9️⃣ Acesse no navegador

- **Admin Django:** http://127.0.0.1:8000/admin
- **API:** http://127.0.0.1:8000/api/

---

## 📁 Estrutura do Projeto

```
gerenciamento-os-django/
├── client/                 # App de Clientes
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── ...
├── employee/              # App de Funcionários
│   ├── models.py
│   ├── views.py
│   └── ...
├── quote/                 # App de Orçamentos
│   ├── models.py
│   ├── views.py
│   └── ...
├── work_order/           # App de Ordens de Serviço
│   ├── models.py
│   ├── views.py
│   └── ...
├── users/                # App de Usuários (Custom User)
│   ├── models.py
│   └── ...
├── core/                 # Configurações principais
│   ├── settings.py       # Configurações de produção
│   ├── settings_test.py  # Configurações para testes
│   ├── urls.py
│   └── wsgi.py
├── scripts/              # Scripts auxiliares
│   ├── populate_postgres.py
│   └── test_endpoints.py
├── tests/                # Testes da API
│   ├── test_api_endpoints.py
│   └── test_api_errors_permissions.py
├── manage.py
├── requirements.txt
├── pytest.ini
├── conftest.py
└── README.md
```

---

## 🔄 Fluxo de Negócio

```
1. Cliente é cadastrado
2. Orçamento é criado com status "aberto"
3. Orçamento pode ser enviado (status "enviado")
4. Cliente aprova orçamento (status "aprovado")
5. Ordem de Serviço é criada a partir do orçamento aprovado
6. OS é executada e seu status muda para "concluído"
```

---

## 📚 Exemplos de Uso

### Via Admin Django

1. Acesse http://127.0.0.1:8000/admin
2. Faça login com seu superuser
3. Navegue pelos apps:
   - **Clients:** Cadastre clientes
   - **Employees:** Gerencie funcionários
   - **Quotes:** Crie e aprove orçamentos
   - **Work Orders:** Crie OS a partir de orçamentos aprovados

### Via API REST

#### 🔐 Autenticação

**1. Obter Token JWT:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "sua_senha"
  }'
```

**Resposta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**2. Renovar Token (quando expirar):**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "SEU_REFRESH_TOKEN"}'
```

---

## 📡 Endpoints da API

### Clients (Clientes)

#### Listar todos os clientes
```bash
GET /client/
Authorization: Bearer SEU_TOKEN
```

**Resposta:**
```json
[
  {
    "id": 1,
    "name": "TechSolutions Brasil LTDA",
    "email": "contato@techsolutions.com.br",
    "cpf_cnpj": "12345678000190",
    "phone": "11987654321"
  }
]
```

#### Criar novo cliente
```bash
POST /client/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Nova Empresa Ltda",
  "email": "contato@empresa.com.br",
  "cpf_cnpj": "12345678000190",
  "phone": "11999999999"
}
```

#### Obter cliente específico
```bash
GET /client/{id}/
Authorization: Bearer SEU_TOKEN
```

#### Atualizar cliente
```bash
PUT /client/{id}/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

#### Deletar cliente
```bash
DELETE /client/{id}/
Authorization: Bearer SEU_TOKEN
```

---

### Employees (Funcionários)

#### Listar todos os funcionários
```bash
GET /employee/
Authorization: Bearer SEU_TOKEN
```

**Resposta:**
```json
[
  {
    "id": 1,
    "name": "Carlos Silva",
    "role": "gerente",
    "phone": "11987654321",
    "user": 1
  }
]
```

#### Criar novo funcionário
```bash
POST /employee/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "name": "João da Silva",
  "role": "operador",
  "phone": "11987654322",
  "user": 2
}
```

**Roles disponíveis:**
- `gerente` - Gerente
- `secretaria` - Secretária
- `operador` - Operador
- `encarregado` - Encarregado

---

### Quotes (Orçamentos)

#### Listar todos os orçamentos
```bash
GET /quote/
Authorization: Bearer SEU_TOKEN
```

**Resposta:**
```json
[
  {
    "id": 1,
    "client": 1,
    "description": "Manutenção de ar condicionado",
    "status": "aprovado",
    "labor_cost": "1500.00",
    "materials_cost": "800.00",
    "total_value": "2300.00"
  }
]
```

#### Criar novo orçamento
```bash
POST /quote/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "client": 1,
  "description": "Serviço de manutenção completa",
  "labor_cost": 500.00,
  "materials_cost": 200.00,
  "status": "aberto"
}
```

**Status disponíveis:**
- `aberto` - Novo orçamento
- `enviado` - Enviado para cliente
- `aprovado` - Aprovado pelo cliente

#### Atualizar status do orçamento
```bash
PUT /quote/{id}/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "status": "aprovado"
}
```

---

### Work Orders (Ordens de Serviço)

#### Listar todas as OGs
```bash
GET /work_order/
Authorization: Bearer SEU_TOKEN
```

**Resposta:**
```json
[
  {
    "id": 1,
    "quote": 1,
    "description": "Execução: Manutenção de ar condicionado",
    "status": "em_andamento",
    "opened_at": "2026-02-17T10:30:00Z",
    "completed_at": null
  }
]
```

#### Criar nova Ordem de Serviço
```bash
POST /work_order/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "quote": 1,
  "description": "Execução do serviço",
  "status": "aberto"
}
```

**⚠️ Importante:** A OS só pode ser criada a partir de um orçamento com status `aprovado`.

**Status disponíveis:**
- `aberto` - Ordem criada
- `em_andamento` - Serviço em execução
- `concluido` - Serviço finalizado

#### Atualizar status da OS
```bash
PUT /work_order/{id}/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "status": "concluido"
}
```

---

### Users (Usuários)

#### Listar todos os usuários
```bash
GET /users/
Authorization: Bearer SEU_TOKEN
```

#### Criar novo usuário
```bash
POST /users/
Content-Type: application/json
```

**Body:**
```json
{
  "email": "novousuario@example.com",
  "password": "senha_forte_123",
  "first_name": "João"
}
```

---

## 🧪 Testes

Execute os testes automatizados com pytest:

```bash
pytest
```

Para ver cobertura de testes:
```bash
pytest --cov=.
```

Os testes estão em:
- `tests/test_api_endpoints.py` - Testes dos endpoints
- `tests/test_api_errors_permissions.py` - Testes de erros e permissões
- Cada app tem seu arquivo `tests.py` com testes específicos

---

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'psycopg2'"

**Solução:**
```bash
pip install -r requirements.txt
```

### Erro ao conectar ao PostgreSQL

**Verifique:**
1. PostgreSQL está rodando?
2. As credenciais no `.env` estão corretas?
3. O banco `gerenciamento_os` existe?

```bash
psql -U postgres -h localhost
\l  # listar bancos
```

### Admin vazio mesmo com dados no banco

**Solução:**
1. Reinicie o servidor Django
2. Verifique se o arquivo `admin.py` registrou os modelos
3. Execute `python manage.py shell` e verifique: `Model.objects.count()`

### Dados diferentes entre Django Shell e Admin

Verifique qual `settings.py` está sendo usado:
```python
from django.conf import settings
print(settings.SETTINGS_MODULE)
```

Deve ser `core.settings` (não `core.settings_test`)

---

## 📊 Modelos Principais

### Client
- name: CharField
- email: EmailField (única)
- cpf_cnpj: CharField
- phone: CharField

### Employee
- user: OneToOneField (User)
- name: CharField
- role: ChoiceField (gerente, secretaria, operador, encarregado)
- phone: CharField

### Quote
- client: ForeignKey
- description: TextField
- status: ChoiceField (aberto, enviado, aprovado)
- labor_cost: DecimalField
- materials_cost: DecimalField
- total_value: computed field

### WorkOrder
- quote: ForeignKey
- description: TextField
- status: ChoiceField (aberto, em_andamento, concluído)
- opened_at: DateTimeField
- completed_at: DateTimeField (nullable)

---

## 📖 Sobre o Projeto

Este sistema foi desenvolvido com foco em simular um fluxo real de gestão de serviços, desde o cadastro do cliente até a finalização da ordem de serviço, aplicando regras de negócio e boas práticas com Django e DRF.

O projeto faz parte do portfólio profissional e demonstra conhecimento em:
- Arquitetura REST
- Autenticação JWT
- Relacionamentos de banco de dados
- Validações de negócio
- Testes automatizados
- Admin Django customizado

---

## 👨‍💻 Autor

**Rafael Feliciano**

- LinkedIn: https://www.linkedin.com/in/rafaelfeliciano-ti/
- GitHub: https://github.com/rafaelfelicianoti

---

## 📄 Licença

Este projeto é de código aberto e está disponível para fins educacionais e comerciais.
