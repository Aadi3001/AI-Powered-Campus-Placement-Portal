from django.contrib import admin
from .models import Company, RecruiterProfile, SkillTag, Job


admin.site.register(Company)
admin.site.register(RecruiterProfile)
admin.site.register(SkillTag)
admin.site.register(Job)
