"""
Script para popular o banco com dados realistas.
Execute no Django shell com: exec(open('populate_data.py').read())
"""
import random
from decimal import Decimal
from django.db import transaction

from users.models import User
from client.models import Client
from employee.models import Employee
from quote.models import Quote
from work_order.models import WorkOrder

# Dados realistas
EMPLOYEE_NAMES = [
    ('Carlos Silva', 'gerente', '11987654321'),
    ('Ana Paula Santos', 'secretaria', '11987654322'),
    ('Roberto Costa', 'operador', '11987654323'),
    ('Mariana Oliveira', 'encarregado', '11987654324'),
    ('Lucas Ferreira', 'operador', '11987654325'),
]

CLIENT_COMPANIES = [
    ('TechSolutions Brasil LTDA', 'contato@techsolutions.com.br', '12345678000190'),
    ('Construção & Cia Serviços', 'contato@construcao.com.br', '98765432000170'),
    ('Indústrias Metalúrgicas São Paulo', 'vendas@metalurgica.com.br', '55443322000150'),
    ('Logística Express Ltda', 'atendimento@logistica.com.br', '33221100000130'),
    ('Reforma & Manutenção Professional', 'orcamento@reforma.com.br', '11223344000190'),
]

SERVICE_DESCRIPTIONS = [
    'Manutenção e limpeza de ar condicionado industrial',
    'Reparo estrutural em estrutura metálica',
    'Instalação de sistema elétrico trifásico',
    'Limpeza e manutenção de tubulações',
    'Inspeção e reparo de equipamentos de elevação',
    'Pintura industrial com tinta epóxi',
    'Serviço de soldagem em aço carbono',
    'Reforma completa de piso industrial',
    'Substituição de correntes de transmissão',
    'Alinhamento de eixos e acoplamentos',
]

with transaction.atomic():
    # Limpar dados antigos se existirem
    Employee.objects.all().delete()
    User.objects.filter(email__startswith='employee').delete()
    Client.objects.all().delete()
    Quote.objects.all().delete()
    WorkOrder.objects.all().delete()
    
    # Criar usuários para employees
    users = []
    print("Criando Employees...")
    for name, role, phone in EMPLOYEE_NAMES:
        email = name.lower().replace(' ', '.') + '@empresa.com.br'
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'is_staff': False}
        )
        emp, created = Employee.objects.get_or_create(
            user=user,
            defaults={
                'name': name,
                'role': role,
                'phone': phone,
            }
        )
        if created:
            print(f"  ✓ {emp.name} ({emp.get_role_display()})")

    # Criar clients
    print("\nCriando Clients...")
    clients = []
    for company_name, email, cnpj in CLIENT_COMPANIES:
        client, created = Client.objects.get_or_create(
            email=email,
            defaults={
                'name': company_name,
                'phone': f'11{random.randint(90000000, 99999999)}',
                'cpf_cnpj': cnpj,
            }
        )
        clients.append(client)
        if created:
            print(f"  ✓ {client.name}")

    # Criar quotes
    print("\nCriando Orçamentos...")
    quotes = []
    for i, description in enumerate(SERVICE_DESCRIPTIONS, 1):
        client = random.choice(clients)
        # Preços mais realistas
        labor = Decimal(random.randint(500, 5000))
        materials = Decimal(random.randint(100, 3000))
        status = random.choice(['aberto', 'enviado', 'aprovado'])
        
        q, created = Quote.objects.get_or_create(
            client=client,
            description=description,
            defaults={
                'status': status,
                'labor_cost': labor,
                'materials_cost': materials,
            }
        )
        quotes.append(q)
        if created:
            total = labor + materials
            print(f"  ✓ {description} - R$ {total:.2f}")

    # Criar work orders só para quotes aprovados
    print("\nCriando Ordens de Serviço...")
    approved = [q for q in quotes if q.status == 'aprovado']
    
    # Se não há aprovados, aprovar alguns
    while len(approved) < 5 and quotes:
        q = random.choice([q for q in quotes if q.status != 'aprovado'])
        q.status = 'aprovado'
        q.save()
        approved = [q for q in quotes if q.status == 'aprovado']

    for q in approved[:5]:
        wo, created = WorkOrder.objects.get_or_create(
            quote=q,
            defaults={
                'description': f'Execução: {q.description}',
                'status': random.choice(['aberto', 'em_andamento', 'concluido']),
            }
        )
        if created:
            print(f"  ✓ OS #{wo.id} - {q.client.name}")

print("\n✅ Dados populados com sucesso!")
