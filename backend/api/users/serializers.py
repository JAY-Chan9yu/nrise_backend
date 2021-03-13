import re

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from api.exceptions import WithdrawalUser
from apps.users.models import User, UserSession


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name')

    def validate_username(self, username):
        code_regex = re.compile('[a-zA-Z|0-9|\-_]')  # 영어 + 숫자 + -,_
        if code_regex.sub('', username):
            raise serializers.ValidationError('유효하지 않은 정규식입니다.', 'regex_error')

        return username

    def validate(self, data):
        if User.objects.filter(username=data.get('username'), withdrawal__isnull=True).exists():
            raise serializers.ValidationError("Username already exists")

        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSession
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'created', 'username', 'withdrawal', 'withdrawal_username')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # sessions 을 따로 지우지 않기때문에 모든 sessions 을 리턴하기에는 부담 (sessions 은 따로 sessions api 에서 조회)
        user_sessions = UserSession.objects.filter(user_id=instance.id)[:10]
        ret['sessions'] = UserSessionSerializer(user_sessions, many=True).data

        return ret


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def validate(self, data):
        # user가 존재하지 않거나, user는 존재하지만 탈퇴한 경우 Login 안됨
        user = authenticate(username=data.get('username'), password=data.get('password'))

        if user is None:
            raise NotFound
        elif user.withdrawal:
            raise WithdrawalUser

        return data


class UUIDCheckSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(required=True)

    class Meta:
        model = UserSession
        fields = ('id', 'uuid')
