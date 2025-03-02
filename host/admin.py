from django.contrib import admin

from .models import GroupEvent,TeamEnrollment,ProjectSubmission,File,Problem,TestCase,IndividualEvent,IndividualEnrollment,HackathonGrading

admin.site.register(GroupEvent)
admin.site.register(TeamEnrollment)
admin.site.register(ProjectSubmission)
admin.site.register(File)
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(IndividualEvent)
admin.site.register(IndividualEnrollment)
admin.site.register(HackathonGrading)