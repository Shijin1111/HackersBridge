from django.urls import path
from . import views
app_name = 'competitor'
urlpatterns = [
    path('dashboard/', views.competitor_dashboard, name='competitor_dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
