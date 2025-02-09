from django.urls import path
from . import views
app_name = 'competitor'
urlpatterns = [
    path('dashboard/', views.competitor_dashboard, name='competitor_dashboard'),
    path('my_teams/',views.my_teams,name = 'my_teams'),
    path('create-team/', views.create_team, name='create_team'),
    path('join-requests/', views.view_join_requests, name='view_join_requests'),
    path('accept-join-request/<int:request_id>/', views.accept_join_request, name='accept_join_request'),
    path('reject-join-request/<int:request_id>/', views.reject_join_request, name='reject_join_request'),
    path('find_group_events/',views.find_group_events,name='find_group_events'),
    path('enroll_in_event/<int:event_id>/', views.enroll_in_event, name='enroll_in_event'),
    path('enrolled_hackathons/', views.enrolled_hackathons, name='enrolled_hackathons'),
    path('event/<int:event_id>/team/<int:team_id>/', views.event_details, name='event_details'),
    path('event/<int:event_id>/submit_project/', views.submit_project, name='submit_project'),
    path('team/<int:team_id>/activities/', views.team_activities, name='team_activities'),
    path('team/<int:team_id>/schedules/', views.schedules, name='schedules'),
    path('team/<int:team_id>/schedule/add/', views.add_session, name='add_session'),
    path('team/<int:team_id>/chat-box/', views.chat_box, name='chat_box'),
    path('team/<int:team_id>/meeting/', views.meeting, name='meeting'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]

