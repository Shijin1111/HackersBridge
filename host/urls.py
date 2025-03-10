from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'host'
urlpatterns = [
    path('dashboard/', views.host_dashboard, name='host_dashboard'),
    path("create-group-event/", views.create_group_event, name="create_group_event"),
    path('create-individual-event/', views.create_individual_event, name='create_individual_event'),
    path('finished_group_events/', views.finished_group_events, name='finished_group_events'),
    path('live-events/', views.live_events, name='live_events'),
    path('event/<int:event_id>/submissions/', views.view_submissions, name='view_submissions'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('grade/<int:submission_id>/', views.grade_project, name='grade_project'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
