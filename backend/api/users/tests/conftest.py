from uuid import uuid4

import pytest

from apps.users.models import User, UserSession


@pytest.fixture(scope='function')
def users_context():
    init_username = 'test_jay'
    init_password = '1q2w3e$R'

    user = User(
        username=init_username,
        name='지찬규',
    )
    user.set_password(init_password)
    user.save()

    user_session = UserSession.objects.create(
        user_id=user.id,
        ip='127.0.0.1',
        uuid=uuid4().__str__()
    )

    init_data = {
        'user': user,
        'session': user_session,
        'init_username': init_username,
        'init_password': init_password
    }

    return init_data
