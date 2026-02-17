#!/usr/bin/env python
"""Script para validar endpoints usando APIClient.

Faz chamadas GET para list/detail e POST para register/login.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from rest_framework.test import APIClient
from django.urls import reverse
from django.conf import settings

client = APIClient()

# permitir testserver no ALLOWED_HOSTS durante os testes
try:
    settings.ALLOWED_HOSTS = ['*']
except Exception:
    pass

def check_get(path):
    resp = client.get(path)
    print(f'GET {path} ->', resp.status_code)
    try:
        print(resp.data)
    except Exception:
        print(resp.content[:200])
    return resp

def check_post(path, data):
    resp = client.post(path, data, format='json')
    print(f'POST {path} ->', resp.status_code)
    try:
        print(resp.data)
    except Exception:
        print(resp.content[:200])
    return resp

def main():
    print('Validando endpoints públicos...')

    # List endpoints
    check_get('/client/')
    check_get('/employee/')
    check_get('/quote/')
    check_get('/work_order/')

    # Detail endpoints (try id 1..5)
    for i in range(1,6):
        check_get(f'/client/{i}/')
        check_get(f'/employee/{i}/')
        check_get(f'/quote/{i}/')
        check_get(f'/work_order/{i}/')

    # Test register and login
    print('\nTestando register/login:')
    reg_data = {'email': 'api_test_user@example.com', 'password': 'testpass123'}
    r = check_post('/users/register/', reg_data)
    if r.status_code == 201:
        print('Registro OK')
    else:
        print('Registro falhou:', r.data)

    login = check_post('/users/login/', reg_data)
    if login.status_code == 200:
        print('Login OK, access token present:', 'access' in login.data)
        token = login.data.get('access')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # testar acesso autenticado (endpoints não exigem, mas testamos)
        print('\nRe-testando /client/ com token:')
        check_get('/client/')
    else:
        print('Login falhou:', login.data)

if __name__ == '__main__':
    main()
