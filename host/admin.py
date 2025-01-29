from django.contrib import admin

from .models import GroupEvent,TeamEnrollment,ProjectSubmission,File

admin.site.register(GroupEvent)
admin.site.register(TeamEnrollment)
admin.site.register(ProjectSubmission)
admin.site.register(File)