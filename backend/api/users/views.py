from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet

from api.paginations import IdOrderingPagination
from api.users.serializers import UserRegisterSerializer, LoginSerializer, UUIDCheckSerializer, \
    UserSessionSerializer, UserSerializer
from api.users.services import UserService
from apps.users.models import User, UserSession


class UserViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    """
        endpoint : /users/
    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = IdOrderingPagination

    def destroy(self, request, *args, **kwargs):
        serializer = UUIDCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_service = UserService()
        data = user_service.withdraw(serializer.data)
        return Response(data=data, status=HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='check')
    def check(self, request, *args, **kwargs):
        username = self.request.GET.get('username')
        user_service = UserService()
        exists = user_service.check_username(username)
        return Response(status=HTTP_400_BAD_REQUEST if exists else HTTP_200_OK)

    @action(detail=False, methods=['put'], url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip = request.META.get('REMOTE_ADDR')
        user_service = UserService()
        data = user_service.login(serializer.data, ip)

        return Response(data=data)

    @action(detail=False, methods=['delete'], url_path='logout')
    def logout(self, request, *args, **kwargs):
        serializer = UUIDCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_service = UserService()
        data = user_service.logout(serializer.data)

        return Response(data=data)

    @action(detail=True, methods=['get'], url_path='sessions')
    def sessions(self, request, *args, **kwargs):
        user = self.get_object()
        user_sessions_qs = UserSession.objects.filter(user_id=user.id)

        page = self.paginate_queryset(user_sessions_qs)
        serializer = UserSessionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
