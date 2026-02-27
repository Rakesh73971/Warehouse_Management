import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create(
        email='manager@gmail.com',
        full_name='Test Manager',
        password='password123',
        role='MANAGER'
    )
    assert user.email == 'manager@gmail.com'
    assert user.is_staff is False


@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(
        email='admin@example.com',
        full_name='Admin user',
        password='password123'
    )

    assert admin.email == 'admin@example.com'
    assert admin.full_name == 'Admin user'
    assert admin.is_staff is True
    assert admin.is_superuser is True
