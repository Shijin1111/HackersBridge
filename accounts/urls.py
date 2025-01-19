from django.urls import path
from . import views

urlpatterns = [
    path('host/login/', views.host_login, name='host_login'),
    path('competitor/login/', views.competitor_login, name='competitor_login'),
]
