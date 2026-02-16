#!/usr/bin/env python
"""
Teste dos endpoints da API usando Django test client
"""
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_test')

import django
django.setup()

from django.test import Client as DjangoClient
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()
client = DjangoClient()

print("\n" + "="*60)
print("TESTANDO ENDPOINTS DA API")
print("="*60)

# Test 1: Register
print("\n[TEST 1] POST /users/register - Registrar novo usuário...")
try:
    response = client.post(
        '/users/register/',
        data=json.dumps({
            'email': 'newuser@example.com',
            'password': 'senha123'
        }),
        content_type='application/json'
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Usuário registrado: {data.get('email')}")
        print(f"   - ID: {data.get('id')}")
        print(f"   - Token de acesso fornecido: {'access' in data}")
    else:
        print(f"❌ Erro: {response.content.decode()}")
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# Test 2: Login
print("\n[TEST 2] POST /users/login - Fazer login...")
try:
    response = client.post(
        '/users/login/',
        data=json.dumps({
            'email': 'newuser@example.com',
            'password': 'senha123'
        }),
        content_type='application/json'
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        access_token = data.get('access')
        print(f"✅ Login realizado!")
        print(f"   - Email: {data.get('user', {}).get('email')}")
        print(f"   - Token de acesso fornecido: {bool(access_token)}")
    else:
        print(f"❌ Erro: {response.content.decode()}")
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# Test 3: GET Clients
print("\n[TEST 3] GET /client/ - Listar clientes...")
try:
    response = client.get('/client/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Clientes recuperados: {len(data)} cliente(s)")
        for client_item in data:
            print(f"   - {client_item.get('name')} ({client_item.get('email')})")
    else:
        print(f"❌ Erro: {response.content.decode()}")
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# Test 4: POST Client
print("\n[TEST 4] POST /client/ - Criar novo cliente...")
try:
    response = client.post(
        '/client/',
        data=json.dumps({
            'name': 'Novo Cliente Teste',
            'email': 'cliente_novo@example.com',
            'phone': '11999999999',
            'cpf_cnpj': '98765432101234'
        }),
        content_type='application/json'
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        client_id = data.get('id')
        print(f"✅ Cliente criado: {data.get('name')} (ID: {client_id})")
    else:
        print(f"❌ Erro: {response.content.decode()}")
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# Test 5: GET Quotes
print("\n[TEST 5] GET /quote/ - Listar orçamentos...")
try:
    response = client.get('/quote/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Orçamentos recuperados: {len(data)} orçamento(s)")
        for quote in data:
            print(f"   - Orçamento #{quote.get('id')}: R$ {quote.get('total_value')}")
    else:
        print(f"❌ Erro: {response.content.decode()}")
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# Test 6: GET Work Orders
print("\n[TEST 6] GET /work_order/ - Listar Ordens de Serviço...")
try:
    response = client.get('/work_order/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Ordens de Serviço recuperadas: {len(data)} OS(s)")
        for wo in data:
            print(f"   - OS #{wo.get('id')}: {wo.get('status')}")
    else:
        print(f"❌ Erro: {response.content.decode()}")
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# Test 7: GET Employees
print("\n[TEST 7] GET /employee/ - Listar funcionários...")
try:
    response = client.get('/employee/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Funcionários recuperados: {len(data)} funcionário(s)")
        for emp in data:
            print(f"   - {emp.get('name')} ({emp.get('role')})")
    else:
        print(f"❌ Erro: {response.content.decode()}")
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

print("\n" + "="*60)
print("TESTES DE API CONCLUÍDOS!")
print("="*60 + "\n")
