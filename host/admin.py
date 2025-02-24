from django.contrib import admin

from .models import GroupEvent,TeamEnrollment,ProjectSubmission,File,Problem,TestCase,IndividualEvent

admin.site.register(GroupEvent)
admin.site.register(TeamEnrollment)
admin.site.register(ProjectSubmission)
admin.site.register(File)
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(IndividualEvent)