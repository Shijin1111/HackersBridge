from django.contrib import admin
from .models import Team,JoinRequest,Session,ProblemResult,IndResult,Payment

admin.site.register(Team)
admin.site.register(JoinRequest)
admin.site.register(Session)
admin.site.register(ProblemResult)
admin.site.register(IndResult)
admin.site.register(Payment)