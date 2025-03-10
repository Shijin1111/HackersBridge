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
    path('find_individual_events/',views.find_individual_events,name='find_individual_events'),
    path('enroll_in_event/<int:event_id>/', views.enroll_in_event, name='enroll_in_event'),
    path('enrolled_hackathons/', views.enrolled_hackathons, name='enrolled_hackathons'),
    path('event/<int:event_id>/team/<int:team_id>/', views.event_details, name='event_details'),
    path('event/<int:event_id>/submit_project/', views.submit_project, name='submit_project'),
    path('team/<int:team_id>/activities/', views.team_activities, name='team_activities'),
    path('team/<int:team_id>/schedules/', views.schedules, name='schedules'),
    path('team/<int:team_id>/schedule/add/', views.add_session, name='add_session'),
    path("chat/", views.chatbox, name="chatbox"),
    path('team/<int:team_id>/meeting/', views.meeting, name='meeting'),
    path('ind_event_dashboard/<int:event_id>/', views.ind_event_dashboard, name='ind_event_dashboard'),
    path('event-expired/', views.ind_event_expiry, name='event_expired_page'),
    path('solve_problem/<int:problem_id>/', views.problem_details, name='solve_problem'),
    path('event/<int:event_id>/submit/', views.submit_event, name='submit_event'),
    path('results/', views.results, name='results'),
    path('ind_results/', views.ind_results, name='ind_results'),
    path('ind_leaderboard/<int:event_id>/',views.ind_leaderboard,name='ind_leaderboard'),
    path('group_results/', views.group_results, name='group_results'),
    path('group_leaderboard/<int:event_id>/',views.group_leaderboard,name='group_leaderboard'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]

