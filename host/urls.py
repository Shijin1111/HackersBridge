from django.urls import path
from . import views
app_name = 'host'
urlpatterns = [
    path('host/dashboard/', views.host_dashboard, name='host_dashboard'),
    path("create-group-event/", views.create_group_event, name="create_group_event"),
]
