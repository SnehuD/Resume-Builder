from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.index, name='home'),
    path('signup.html',views.sign_up, name='sign-up'),
    path('signin.html',views.sign_in, name='sign-in'),
    path('signup',views.signup_con, name='signup_con'),
    path('signin',views.signin_con, name='signin_con'),
    path('verification', views.verification, name="verification"),
    path('resend_ver_email', views.resend_ver_email, name='resend_verification_email'),
    path('forgot-password.html',views.fp, name='Forgot_Password'),
    path('forgot-password',views.forgot_password, name='Forgot_Password_Controller'),
    path('dashboard', views.dashboard, name='Dashboard'),
    path('logout', views.logout, name='Logout'),
    path('updateprofile/<int:id>', views.update_profile, name='update_profile'),
    path('deleteprofile/<int:id>', views.delete_profile, name='delete_profile')
]