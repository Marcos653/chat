from .models import *

from rest_framework import serializers
from drf_base64.fields import Base64ImageField, Base64FileField


class UserSerializer(serializers.ModelSerializer):
    image_user = Base64ImageField(required=False)
    old_password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)

        if password is not None and not instance.check_password(old_password):
            pass
        if password is not None:
            instance.set_password(password)

        new_instance = super().update(instance, validated_data)
        return new_instance

    class Meta:
        model = User
        fields = '__all__'