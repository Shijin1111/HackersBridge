from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('problems/<int:problem_id>/', views.problem_details, name='problem_details'),
]
