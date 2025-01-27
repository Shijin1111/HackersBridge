from django.urls import path
from . import views
app_name = 'host'
urlpatterns = [
    path('dashboard/', views.host_dashboard, name='host_dashboard'),
    path("create-group-event/", views.create_group_event, name="create_group_event"),
    path('logout/', views.logout_view, name='logout'),
]
