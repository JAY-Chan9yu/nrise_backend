import pytest

from api.users.services import UserService
from apps.users.models import UserSession, User

LOGIN_DATA_FIELDS = ['id', 'user_id', 'ip', 'uuid']
WITHDRAWAL_DATA_FIELDS = ['id', 'created', 'withdrawal', 'withdrawal_username']


@pytest.mark.django_db
def test_user_service_check_name(users_context):
    username = users_context.get('init_username')
    user_service = UserService()
    exists = user_service.check_username(username)

    assert exists is True


@pytest.mark.django_db
def test_user_service_login(users_context):
    data = {
        'username': users_context.get('init_username'),
        'password': users_context.get('init_password'),
    }
    user_service = UserService()
    login_data = user_service.login(user_data=data, ip='127.0.0.1')

    assert list(login_data.keys()) == LOGIN_DATA_FIELDS
    assert UserSession.objects.filter(uuid=login_data.get('uuid')).exists()


@pytest.mark.django_db
def test_user_service_logout(users_context):
    data = {
        'uuid': users_context.get('session').uuid,
    }
    user_service = UserService()
    user_service.logout(data)

    assert UserSession.objects.filter(uuid=data.get('uuid'), last_logout__isnull=False).exists()
    assert User.objects.filter(id=users_context.get('session').user_id, last_logout__isnull=False).exists()


@pytest.mark.django_db
def test_user_service_withdraw(users_context):
    data = {
        'uuid': users_context.get('session').uuid,
    }
    user_service = UserService()
    withdraw_data = user_service.withdraw(data)

    assert list(withdraw_data.keys()) == WITHDRAWAL_DATA_FIELDS
    assert User.objects.filter(
        withdrawal_username=withdraw_data.get('withdrawal_username'),
        withdrawal=withdraw_data.get('withdrawal')
    ).exists()

    assert UserSession.objects.filter(
        uuid=data.get('uuid'), last_logout__isnull=False
    ).exists()
