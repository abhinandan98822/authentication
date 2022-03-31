from unicodedata import name
from django.urls import path
# from django.conf import settings
from .views import ChangePassword, activate,forgotP
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.registerform,name='registerform'),
    path('login/',views.loginform,name='login'),
    path('forgot/',views.forgotpassword,name='forgot'),
    path('forgotP/<uidb64>/<token>/',
         forgotP,name='forgotP'),
    path('homepage/',views.home,name='homepage'),
    path('confirmR',views.confirm,name='confirmR'),
    path('activate/<uidb64>/<token>/',  
        activate, name='activate'), 
    path('',views.index,name='index'),
    path('changeP/',views.ChangePassword,name='changepassword') ,
    path('CPD/',views.ChangePasswordDone,name='CPD'),
    path('fps/',views.forgotpasswordchange,name='fps'),
    path('password_reset_confirm/<uidb64>/<token>/',  
        forgotP, name='password_reset_confirm'), 
    
]