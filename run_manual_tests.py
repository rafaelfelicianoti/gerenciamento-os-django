#!/usr/bin/env python
"""
Script de teste para verificar se os modelos e serializers funcionam
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_test')

import django
django.setup()

from users.models import User
from client.models import Client
from employee.models import Employee
from quote.models import Quote
from work_order.models import WorkOrder
from decimal import Decimal

print("\n" + "="*60)
print("TESTANDO MODELOS E SERIALIZERS")
print("="*60)

# Test 1: Criar usuário
print("\n[TEST 1] Criando usuário...")
try:
    user = User.objects.create_user(
        email='test@example.com',
        password='password123'
    )
    print(f"✅ Usuário criado: {user.email}")
except Exception as e:
    print(f"❌ Erro ao criar usuário: {e}")

# Test 2: Criar cliente
print("\n[TEST 2] Criando cliente...")
try:
    client = Client.objects.create(
        name='Empresa Teste',
        email='empresa@example.com',
        phone='11987654321',
        cpf_cnpj='12345678901234'
    )
    print(f"✅ Cliente criado: {client.name}")
except Exception as e:
    print(f"❌ Erro ao criar cliente: {e}")

# Test 3: Criar funcionário
print("\n[TEST 3] Criando funcionário com usuário...")
try:
    employee = Employee.objects.create(
        user=user,
        name='João da Silva',
        role='operador',
        phone='11987654321'
    )
    print(f"✅ Funcionário criado: {employee.name} ({employee.role})")
except Exception as e:
    print(f"❌ Erro ao criar funcionário: {e}")

# Test 4: Criar orçamento
print("\n[TEST 4] Criando orçamento...")
try:
    quote = Quote.objects.create(
        client=client,
        description='Serviço de manutenção',
        status='aberto',
        labor_cost=Decimal('100.00'),
        materials_cost=Decimal('50.00')
    )
    print(f"✅ Orçamento criado: #{quote.id}")
    print(f"   - Custo mão de obra: R$ {quote.labor_cost}")
    print(f"   - Custo materiais: R$ {quote.materials_cost}")
    print(f"   - Total: R$ {quote.total_value}")
except Exception as e:
    print(f"❌ Erro ao criar orçamento: {e}")

# Test 5: Aprovar orçamento e criar OS
print("\n[TEST 5] Aprovando orçamento e criando Ordem de Serviço...")
try:
    quote.status = 'aprovado'
    quote.save()
    
    work_order = WorkOrder.objects.create(
        quote=quote,
        description='Executar manutenção conforme orçamento',
        status='aberto'
    )
    print(f"✅ Ordem de Serviço criada: #{work_order.id}")
    print(f"   - Status: {work_order.status}")
    print(f"   - Valor total: R$ {work_order.total_value}")
except Exception as e:
    print(f"❌ Erro ao criar OS: {e}")

# Test 6: Testar serializers
print("\n[TEST 6] Testando serializers...")
try:
    from users.serializers import UserSerializer, RegisterSerializer
    from client.serializers import ClientSerializer
    from employee.serializers import EmployeeSerializer
    from quote.serializers import QuoteSerializer
    from work_order.serializers import WorkOrderSerializer
    
    user_data = UserSerializer(user).data
    print(f"✅ UserSerializer: {user_data}")
    
    client_data = ClientSerializer(client).data
    print(f"✅ ClientSerializer: {client_data['name']}")
    
    quote_data = QuoteSerializer(quote).data
    print(f"✅ QuoteSerializer: Orçamento #{quote_data['id']}")
    
    work_order_data = WorkOrderSerializer(work_order).data
    print(f"✅ WorkOrderSerializer: OS #{work_order_data['id']}")
    
except Exception as e:
    print(f"❌ Erro ao testar serializers: {e}")

# Test 7: Testar validações
print("\n[TEST 7] Testando validações de WorkOrder...")
try:
    # Tentar criar OS com orçamento não aprovado
    quote_not_approved = Quote.objects.create(
        client=client,
        description='Teste',
        status='aberto',
        labor_cost=Decimal('50.00'),
        materials_cost=Decimal('25.00')
    )
    
    try:
        bad_work_order = WorkOrder.objects.create(
            quote=quote_not_approved,
            description='Teste',
            status='aberto'
        )
        print(f"❌ Deveria ter falhado mas criou!")
    except Exception as validation_error:
        print(f"✅ Validação funcionou: {validation_error}")
        
except Exception as e:
    print(f"⚠️  Erro no teste: {e}")

print("\n" + "="*60)
print("TESTES CONCLUÍDOS!")
print("="*60 + "\n")
