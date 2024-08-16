from django.urls import include, path
from rest_framework import routers
from .views import *
from . import views

router = routers.DefaultRouter()

# specify URL Path for rest_framework
urlpatterns = [
    
    path('generate/', views.generate_and_save_qr, name='generate_and_save_qr'),
    path('get/<int:pk>/', views.qr_code_detail, name='qr_code_detail'),
    path('add/<int:pk>/', views.qr_code_update, name='qr_code_update'),
    path('api/', views.my_view, name='qr_code_update'),
    
]