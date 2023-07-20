from typing import ClassVar
from django.conf import settings
from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from account.models import User, ValidationCode

class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        # fields = ['id','username','password','email','first_name','last_name',
        # ]
        fields = ['username','password']

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','first_name','last_name','password']

class UserVerifySerializer(serializers.Serializer):
    code =serializers.IntegerField()
    username = serializers.CharField()



class UserPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        #you can add your more data with this and return
        data['username'] = str(self.user.username)

        return data
