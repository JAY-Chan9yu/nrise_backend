from apps.users.models import User


class UserService(object):

    def check_username(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()
