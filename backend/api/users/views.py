from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from api.users.serializers import UserRegisterSerializer
from api.users.services import UserService
from apps.users.models import User


class UserViewSet(mixins.CreateModelMixin,
                  GenericViewSet):
    """
        endpoint : /users/
    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny, )

    # https://www.django-rest-framework.org/api-guide/routers/#routing-for-extra-actions 참고
    @action(detail=False, methods=['get'], url_path='check')
    def check(self, request, *args, **kwargs):
        username = self.request.GET.get('username')
        user_service = UserService()
        exists = user_service.check_username(username)
        return Response(status=HTTP_400_BAD_REQUEST if exists else HTTP_200_OK)
