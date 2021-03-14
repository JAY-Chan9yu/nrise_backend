from datetime import datetime
from uuid import uuid4

from django.contrib.auth import authenticate
from rest_framework.exceptions import NotFound

from api.exceptions import WithdrawalUser, AlreadyLogout
from apps.users.models import User, UserSession


class UserService(object):

    def check_username(self, username: str) -> bool:
        return User.objects.filter(username=username, withdrawal__isnull=True).exists()

    def login(self, user_data: dict, ip: str) -> dict:
        # user가 존재하지 않거나, user는 존재하지만 탈퇴한 경우 Login 안됨
        user = authenticate(username=user_data.get('username'), password=user_data.get('password'))

        if user is None:
            raise NotFound
        elif user.withdrawal:
            raise WithdrawalUser

        # UserSession 생성
        user_session = UserSession.objects.create(
            user_id=user.id,
            ip=ip,
            uuid=uuid4().__str__()
        )

        data = {
            'id': user_session.id,
            'user_id': user_session.user_id,
            'ip': user_session.ip,
            'uuid': user_session.uuid,
        }

        return data

    def logout(self, data: dict):
        try:
            user_session = UserSession.objects.prefetch_related('user').get(uuid=data.get('uuid'))
        except UserSession.DoesNotExist:
            raise NotFound

        if user_session.last_logout:
            raise AlreadyLogout

        now = datetime.now()
        user_session.last_logout = now
        user_session.save(update_fields=['last_logout'])

        user_session.user.last_logout = now
        user_session.user.save(update_fields=['last_logout'])

        return data

    def withdraw(self, data: dict):
        try:
            user_session = UserSession.objects.prefetch_related('user').get(uuid=data.get('uuid'))
        except UserSession.DoesNotExist:
            raise NotFound

        if user_session.user.withdrawal:
            raise WithdrawalUser

        # 탈퇴 + last_logout 업데이트
        now = datetime.now()
        user_session.last_logout = now
        user_session.save(update_fields=['last_logout'])

        """
        username 을 재정의해서 unique=False로 정하려다가 관리가 안되는경우 동일한 username 생성 후 꼬이는 경우가 발생될 것 같아
        회원탈퇴시 username=None, withdrawal_username에 usename을 기록했습니다. 
        - 탈퇴인 유저 : withdrawal + withdrawal_username, username=None )
        """
        user_session.user.last_logout = now
        user_session.user.withdrawal = now
        user_session.user.withdrawal_username = user_session.user.username
        user_session.user.username = None
        user_session.user.save(update_fields=['withdrawal', 'withdrawal_username', 'last_logout', 'username'])

        data = {
            'id': user_session.user.id,
            'created': user_session.user.created,
            'withdrawal': user_session.user.withdrawal,
            'withdrawal_username': user_session.user.withdrawal_username,
        }
        return data
