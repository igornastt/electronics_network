from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User
from users.validators import EmailValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'country', 'city', 'password', 'is_active')

    @staticmethod
    def validate_password(value):
        return make_password(value)


class UserCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        validators = [
            EmailValidator(field="email")
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User.objects.create(**validated_data)
        instance.is_active = True

        if password is not None:
            new_pwd = make_password(password)
            instance.set_password(new_pwd)
        instance.save()

        return instance
