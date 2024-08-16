from django.urls import path
from .views import AdminRegisterView, AdminLoginView, AdminLogoutView

urlpatterns = [
    path('register/new/', AdminRegisterView.as_view(), name='admin-register'),
    path('login/new/', AdminLoginView.as_view(), name='admin-login'),
    path('logout/new/', AdminLogoutView.as_view(), name='admin-logout'),
]
