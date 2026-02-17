import pytest
from rest_framework.test import APIClient

from client.models import Client
from quote.models import Quote


@pytest.fixture
def api_client():
    return APIClient()


def test_client_put_email_conflict(api_client, db):
    # create two clients
    a = api_client.post('/client/', {'name': 'A', 'email': 'a@example.com', 'phone': '11900000001', 'cpf_cnpj': '111'}, format='json')
    assert a.status_code == 201
    b = api_client.post('/client/', {'name': 'B', 'email': 'b@example.com', 'phone': '11900000002', 'cpf_cnpj': '222'}, format='json')
    assert b.status_code == 201

    bid = b.data['id']

    # attempt to update B's email to A's email -> should fail (unique)
    r = api_client.put(f'/client/{bid}/', {'name': 'B', 'email': 'a@example.com', 'phone': '11900000002', 'cpf_cnpj': '222'}, format='json')
    assert r.status_code == 400
    assert 'email' in r.data or 'unique' in str(r.data).lower()


def test_workorder_create_and_put_with_invalid_quote(api_client, db):
    # create client and quotes
    client = Client.objects.create(name='C', email='c@example.com', phone='11911110000', cpf_cnpj='333')
    approved = Quote.objects.create(client=client, description='ok', status='aprovado', labor_cost='10.00', materials_cost='5.00')
    not_approved = Quote.objects.create(client=client, description='no', status='aberto', labor_cost='1.00', materials_cost='1.00')

    # create workorder for approved quote
    r = api_client.post('/work_order/', {'quote': approved.id, 'description': 'do it'}, format='json')
    assert r.status_code == 201
    wid = r.data['id']

    # attempt to update workorder to reference not_approved quote -> should fail validation
    r2 = api_client.put(f'/work_order/{wid}/', {'quote': not_approved.id, 'description': 'updated'}, format='json')
    assert r2.status_code == 400
    assert 'quote' in r2.data or 'orcamento' in str(r2.data).lower()


def test_endpoints_access_with_and_without_jwt(api_client, db):
    # register and login to get token
    reg = api_client.post('/users/register/', {'email': 'perm@example.com', 'password': 'perm1234'}, format='json')
    assert reg.status_code == 201
    login = api_client.post('/users/login/', {'email': 'perm@example.com', 'password': 'perm1234'}, format='json')
    assert login.status_code == 200
    token = login.data.get('access')

    # endpoint access without token (should be public)
    r_no = api_client.get('/client/')
    assert r_no.status_code == 200

    # endpoint access with token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    r_yes = api_client.get('/client/')
    assert r_yes.status_code == 200
