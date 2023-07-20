from django.db import router
from django.urls import path
from rest_framework import routers
from rest_framework_nested import routers
from . import views

app_name = "account"
router = routers.DefaultRouter()
router.register('verify-code',views.CustomLoginView)

urlpatterns = [
    path("api/send-phone",views.sendCodeView.as_view(),name="send_phone"),
    # path("api/verify-code",views.CustomLoginView.as_view(),name="verify_code"),
    

 ] + router.urls
