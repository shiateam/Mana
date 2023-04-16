from random import randint
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView 
from kavenegar import *
from rest_framework.response import Response
from account.models import User, ValidationCode
from account.serializers import CustomTokenObtainPairSerializer, UserPhoneSerializer, UserVerifySerializer
from account.authentication import *
from rest_framework import status
from djoser.views import UserViewSet
from djoser import signals
from djoser.compat import get_user_email
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class sendCodeView(APIView):

    def post (self ,request):
        serializer = UserPhoneSerializer(data = request.data)
        if serializer.is_valid():
            phone = request.data['phone'] 
            print (phone)
            user = User.objects.filter(username =phone).first() 
            print(user.id)
            if user is None:
                return Response(message =  f"{phone} موجود نیست ", status=status.HTTP_400_BAD_REQUEST)         
            try:
                    code = randint(100000,999999)
                    ValidationCode.objects.create(mobile=phone,validation_code=code)
                    api = KavenegarAPI('4B4C594D2B716F366F6938686B4165732B6D54564F3979476F70642F68706A7863365445762F7A75636A453D')
                    params = {
                    'sender': '',
                    'receptor': f"{phone}",
                    'message': code
                        }
                    response = api.sms_send(params)
                    print
                    str(response)
                    return Response({'username':user.username},status=status.HTTP_200_OK)
            except APIException as e:
                    print
                    str(e)
            except HTTPException as e:
                    print
                    str(e)
        return Response(status=status.HTTP_404_NOT_FOUND)


    
# class loginWithPhoneView(APIView):

#     def post (self ,request):
#         serializer = UserVerifySerializer(data = request.data)
#         if serializer.is_valid():
#             code = request.data['code']
#             username= request.data['username']
#             validation_code = ValidationCode.objects.get(mobile=username,validation_code=code).validation_code
#             user = User.objects.get(username = username) 
#             if validation_code == code:
#                 refresh = RefreshToken.for_user(user)
#                 data = {
#                          'refresh': str(refresh),
#                          'access': str(refresh.access_token)
#                     }
#                 ValidationCode.objects.get(mobile=username,validation_code=code).delete()
#                 return Response(data=data,status=status.HTTP_201_CREATED)
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status= status.HTTP_400_BAD_REQUEST)
                
class CustomLoginView(UserViewSet):

    def perform_create(self, serializer):
        user = serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = UserVerifySerializer(data = request.data)
        print(serializer)
        if serializer.is_valid():
            # self.perform_create(serializer)
            # headers = self.get_success_headers(serializer.data)
            print(serializer)
            code = request.data['code']
            username= request.data['username']
            print(username)
            validation_code = ValidationCode.objects.get(mobile=username,validation_code=code).validation_code
            user = User.objects.get(username = username) 
            if validation_code == code:
                refresh = RefreshToken.for_user(user)
                data = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                        }
                ValidationCode.objects.get(mobile=username,validation_code=code).delete()
                return Response(data=data,status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status= status.HTTP_400_BAD_REQUEST)
    

