import pytest
from users.models import User

# funcao para criar o usuario nos testes e nao precisar ficar repetindo codigo
@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="teste@gmail.com",
        password="1234"

    )