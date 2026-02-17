import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from users.models import User
from client.models import Client
from quote.models import Quote


@pytest.fixture
def api_client():
    return APIClient()


def test_client_crud(api_client, db):
    # create
    data = {
        'name': 'API Cliente',
        'email': 'api_client@example.com',
        'phone': '11999990000',
        'cpf_cnpj': '99999999999'
    }
    r = api_client.post('/client/', data, format='json')
    assert r.status_code == 201
    cid = r.data['id']

    # list
    r = api_client.get('/client/')
    assert r.status_code == 200
    assert any(c['id'] == cid for c in r.data)

    # detail
    r = api_client.get(f'/client/{cid}/')
    assert r.status_code == 200

    # update
    r = api_client.put(f'/client/{cid}/', {'name': 'API Cliente Updated', 'email': data['email'], 'phone': data['phone'], 'cpf_cnpj': data['cpf_cnpj']}, format='json')
    assert r.status_code == 201 or r.status_code == 200
    assert r.data['name'] == 'API Cliente Updated'

    # delete
    r = api_client.delete(f'/client/{cid}/')
    assert r.status_code in (204,)


def test_employee_crud(api_client, db):
    # create employee (creates user)
    data = {
        'name': 'API Emp',
        'role': 'operador',
        'phone': '11988880000',
        'email': 'api_emp@example.com',
        'password': 'pass1234'
    }
    r = api_client.post('/employee/', data, format='json')
    assert r.status_code == 201
    eid = r.data['id']

    # detail
    r = api_client.get(f'/employee/{eid}/')
    assert r.status_code == 200
    assert r.data['email'] == data['email']

    # partial update
    r = api_client.put(f'/employee/{eid}/', {'role': 'encarregado'}, format='json')
    assert r.status_code == 200

    # delete and ensure user removed
    r = api_client.delete(f'/employee/{eid}/')
    assert r.status_code == 204


def test_workorder_creation_and_validation(api_client, db):
    # create client and approved quote via ORM
    client = Client.objects.create(name='WO Client', email='wo_client@example.com', phone='11977770000', cpf_cnpj='77777777777')
    approved = Quote.objects.create(client=client, description='Approved', status='aprovado', labor_cost='100.00', materials_cost='50.00')

    # create workorder for approved quote
    r = api_client.post('/work_order/', {'quote': approved.id, 'description': 'Exec via API'}, format='json')
    assert r.status_code == 201
    wid = r.data['id']

    # update
    r = api_client.put(f'/work_order/{wid}/', {'description': 'Changed', 'quote': approved.id, 'status': 'em_andamento'}, format='json')
    assert r.status_code == 200
    assert r.data['description'] == 'Changed'

    # delete
    r = api_client.delete(f'/work_order/{wid}/')
    assert r.status_code == 204

    # validation: cannot create with non-approved quote
    not_approved = Quote.objects.create(client=client, description='NA', status='aberto', labor_cost='10.00', materials_cost='5.00')
    r = api_client.post('/work_order/', {'quote': not_approved.id, 'description': 'Should fail'}, format='json')
    assert r.status_code == 400
