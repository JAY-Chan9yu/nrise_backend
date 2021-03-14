import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from apps.users.models import UserSession
from request_helper import pytest_request


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_name_check_200(rf, users_context):
    data = {
        'username': 'test_jay_2'
    }
    url = reverse(viewname="users-check")
    response = pytest_request(rf,
                              method='get',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_create_201(rf, users_context):
    data = {
        "username": "nrise",
        "password": "111111",
        "name": "엔라이즈"
    }
    url = reverse(viewname="users-list")
    response = pytest_request(rf,
                              method='post',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_login_200(rf, users_context):
    data = {
        "username": users_context.get('init_username'),
        "password": users_context.get('init_password'),
    }
    url = reverse(viewname="users-login")
    response = pytest_request(rf,
                              method='put',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_logout_204(rf, users_context):
    data = {
        'uuid': users_context.get('session').uuid
    }
    url = reverse(viewname="users-logout")
    response = pytest_request(rf,
                              method='delete',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_delete_204(rf, users_context):
    user_id = users_context.get('user').id
    data = {
        'uuid': users_context.get('session').uuid
    }
    url = reverse(viewname="users-detail", kwargs={'pk': user_id})
    response = pytest_request(rf,
                              method='delete',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_list_200(rf, users_context):
    user_id = users_context.get('user').id
    url = reverse(viewname="users-detail", kwargs={'pk': user_id})
    response = pytest_request(rf,
                              method='get',
                              url=url,
                              user=None)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_session_200(rf, users_context):
    user_id = users_context.get('user').id
    url = reverse(viewname="users-sessions", kwargs={'pk': user_id})
    response = pytest_request(rf,
                              method='get',
                              url=url,
                              user=None)

    assert response.status_code == status.HTTP_200_OK
