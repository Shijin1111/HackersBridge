from django.urls import path
from . import views
app_name = 'competitor'
urlpatterns = [
    path('dashboard/', views.competitor_dashboard, name='competitor_dashboard'),
    path('my_teams/',views.my_teams,name = 'my_teams'),
    path('create-team/', views.create_team, name='create_team'),
    path('logout/', views.logout_view, name='logout'),
]
