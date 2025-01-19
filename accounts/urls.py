from django.urls import path
from . import views

urlpatterns = [
    path('host/login/', views.host_login, name='host_login'),
    path('competitor/login/', views.competitor_login, name='competitor_login'),
    path('host/dashboard/', views.host_dashboard, name='host_dashboard'),
    path('competitor/dashboard/', views.competitor_dashboard, name='competitor_dashboard'),
]
