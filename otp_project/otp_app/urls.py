from django.urls import path
from . import views

urlpatterns = [
    path('enter-phone/', views.mobile_verification, name='enter_phone'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('success/', views.success_page, name='success'),
]

