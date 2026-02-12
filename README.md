# Sistema de Gerenciamento de Ordens de Serviço

Sistema web desenvolvido em Django para controle de clientes, orçamentos e ordens de serviço, permitindo a criação de OS apenas a partir de orçamentos aprovados.

---

## 📌 Funcionalidades

- Cadastro de clientes
- Gerenciamento de usuários com autenticação personalizada
- Criação e gerenciamento de orçamentos
- Aprovação de orçamentos
- Geração de ordens de serviço vinculadas a orçamentos aprovados
- Controle de status das OS
- Painel administrativo com Django Admin

---

## 🚀 Tecnologias

- Python 3
- Django
- PostgreSQL
- Django Rest Framework
- Git

---

## ✅ Requisitos

- Python 3.10+
- PostgreSQL
- Git

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

Ativação no Linux/Mac:

```bash
source venv/bin/activate
```

Ativação no Windows:

```bash
venv\Scripts\activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_NAME=seubanco
DB_USER=seuusuario
DB_PASSWORD=suasenha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=sua_chave_secreta
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

### 7️⃣ Inicie o servidor

```bash
python manage.py runserver
```

### 8️⃣ Acesse no navegador

```
http://127.0.0.1:8000/admin
```

---

## 📁 Estrutura do Projeto

```bash
gerenciamento_os/
├── client/
├── employee/
├── quote/
├── users/
├── work_order/
├── core/
├── manage.py
└── requirements.txt
```

---

## 📖 Sobre o Projeto

Este sistema foi desenvolvido com foco em simular um fluxo real de gestão de serviços, desde o cadastro do cliente até a finalização da ordem de serviço, aplicando regras de negócio e boas práticas com Django.

O projeto faz parte do meu portfólio profissional.

---

## 👨‍💻 Autor

**Rafael Feliciano**

- LinkedIn: https://www.linkedin.com/in/rafaelfeliciano-ti/
- GitHub: https://github.com/rafaelfelicianoti
