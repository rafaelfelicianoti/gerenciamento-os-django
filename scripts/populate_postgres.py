#!/usr/bin/env python
"""Popula o banco configurado em `core.settings` com dados de exemplo.

Gera:
- 5 Clients
- 5 Employees (cada um com um User)
- 10 Quotes (distribuídos entre clients)
- 5 WorkOrders (para orçamentos aprovados)

Use: `python scripts/populate_postgres.py` (assegure variáveis de BD em env)
"""
import os
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.db import transaction
from users.models import User
from client.models import Client
from employee.models import Employee
from quote.models import Quote
from work_order.models import WorkOrder


def create_sample_data(
    n_clients=5, n_employees=5, n_quotes=10, n_workorders=5
):
    with transaction.atomic():
        clients = []
        for i in range(1, n_clients + 1):
            email = f'client{i}@example.com'
            cpf = f'{10000000000 + i}'
            client, _ = Client.objects.get_or_create(
                email=email,
                defaults={
                    'name': f'Empresa {i}',
                    'phone': f'1190000{i:04d}',
                    'cpf_cnpj': cpf,
                }
            )
            clients.append(client)

        employees = []
        roles = [c[0] for c in Employee.ROLE_CHOICES]
        for i in range(1, n_employees + 1):
            email = f'employee{i}@example.com'
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={'is_staff': False}
            )
            # set a password if newly created
            if not user.has_usable_password():
                user.set_password('password123')
                user.save()

            emp, _ = Employee.objects.get_or_create(
                user=user,
                defaults={
                    'name': f'Funcionário {i}',
                    'role': random.choice(roles),
                    'phone': f'1191000{i:04d}',
                }
            )
            employees.append(emp)

        quotes = []
        for i in range(1, n_quotes + 1):
            client = random.choice(clients)
            labor = Decimal(random.randint(50, 500))
            materials = Decimal(random.randint(10, 300))
            status = random.choice(['aberto', 'enviado', 'aprovado'])
            q = Quote.objects.create(
                client=client,
                description=f'Serviço exemplo #{i}',
                status=status,
                labor_cost=Decimal(f'{labor}.00'),
                materials_cost=Decimal(f'{materials}.00'),
            )
            quotes.append(q)

        # create workorders only for approved quotes (or approve some)
        approved = [q for q in quotes if q.status == 'aprovado']
        # if not enough approved, approve some
        while len(approved) < n_workorders and quotes:
            q = random.choice(quotes)
            q.status = 'aprovado'
            q.save()
            approved = [q for q in quotes if q.status == 'aprovado']

        workorders = []
        for i in range(min(n_workorders, len(approved))):
            q = approved[i]
            wo = WorkOrder.objects.create(
                quote=q,
                description=f'Execução do {q.description}',
                status='aberto'
            )
            workorders.append(wo)

    return {
        'clients': clients,
        'employees': employees,
        'quotes': quotes,
        'workorders': workorders,
    }


if __name__ == '__main__':
    print('Populando banco definido em core.settings com dados de exemplo...')
    try:
        res = create_sample_data()
        print('Criado:')
        print(f" - Clients: {len(res['clients'])}")
        print(f" - Employees: {len(res['employees'])}")
        print(f" - Quotes: {len(res['quotes'])}")
        print(f" - WorkOrders: {len(res['workorders'])}")
    except Exception as e:
        print('Erro ao popular o banco:', e)
        raise
