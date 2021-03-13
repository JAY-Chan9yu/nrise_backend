from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeModelMixin


class User(TimeModelMixin, auth_models.AbstractUser):
    name = models.CharField(verbose_name='name', max_length=50)
    last_logout = models.DateTimeField(_('last logout'), blank=True, null=True)

    class Meta:
        verbose_name = 'user'

    def __str__(self):
        return "name: {}".format(self.username)


class UserSession(TimeModelMixin):
    """
        User 세션 관리를 위한 모델
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_logout = models.DateTimeField(_('last logout'), blank=True, null=True)
    ip = models.CharField(_('ip'), max_length=135, null=False) # IPv6 추후 고려해서 128bit + 중간 구분 문자 7bit
    uuid = models.CharField(max_length=36) # uuid4 사용

    class Meta:
        verbose_name = 'user session'
