from datetime import datetime

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from request_helper import pytest_request


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_name_check_400(rf, users_context):
    data = {
        'username': users_context.get('user').username
    }
    url = reverse(viewname="users-check")
    response = pytest_request(rf,
                              method='get',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_create_400(rf, users_context):
    data = {
        "username": users_context.get('user').username,
        "password": "111111",
        "name": "엔라이즈"
    }
    url = reverse(viewname="users-list")
    response = pytest_request(rf,
                              method='post',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_login_404(rf, users_context):
    data = {
        "username": users_context.get('init_username'),
        "password": '111111',
    }
    url = reverse(viewname="users-login")
    response = pytest_request(rf,
                              method='put',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.urls(urls='api.urls')
@pytest.mark.django_db
def test_user_logout_403(rf, users_context):
    data = {
        'uuid': users_context.get('session').uuid
    }
    session = users_context.get('session')
    session.last_logout = datetime.now()
    session.save(update_fields=['last_logout'])

    url = reverse(viewname="users-logout")
    response = pytest_request(rf,
                              method='delete',
                              url=url,
                              user=None,
                              data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
