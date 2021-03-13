import re

from rest_framework import serializers

from apps.users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'name')

    def validate_username(self, username):
        code_regex = re.compile('[a-zA-Z|0-9|\-_]')  # 영어 + 숫자 + -,_
        if code_regex.sub('', username):
            raise serializers.ValidationError('유효하지 않은 정규식입니다.', 'regex_error')

        return username

    def validate(self, data):
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError("Username already exists")

        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            name=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
