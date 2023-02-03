from typing import ClassVar
from django.conf import settings
from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        # fields = ['id','username','password','email','first_name','last_name',
        # ]
        fields = ['username','password']

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','first_name','last_name','password']