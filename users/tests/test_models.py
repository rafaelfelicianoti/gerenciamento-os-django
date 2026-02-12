import pytest
from users.models import User

# Criacao usuario
@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="teste@gmail.com",
        password="1234"
    )

    assert user.email == "teste@gmail.com"
    assert user.check_password("1234") is True
    assert user.is_active is True
    assert user.is_staff is False


import pytest
from users.models import User

# Se nao fornecer email
@pytest.mark.django_db
def test_create_user_without_email_raises_error():
    with pytest.raises(ValueError) as excinfo:
        User.objects.create_user(email=None, password="123456")
    assert "e-mail é obrigatorio" in str(excinfo.value)

# Criacao do superuser
@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        password="admin123"
    )
    assert admin.is_staff is True
    assert admin.is_superuser is True
