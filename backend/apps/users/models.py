from django.contrib.auth import models as auth_models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeModelMixin


class User(TimeModelMixin, auth_models.AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        default=None,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(verbose_name='name', max_length=50)
    last_logout = models.DateTimeField(_('last logout'), blank=True, null=True)
    withdrawal = models.DateTimeField(_('withdrawal'), blank=True, null=True) # 회원탈퇴 시간
    withdrawal_username = models.CharField(_('withdrawal_username'), max_length=150, null=True, default=None) # 탈퇴한 ID

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
        ordering = ('-id',)
