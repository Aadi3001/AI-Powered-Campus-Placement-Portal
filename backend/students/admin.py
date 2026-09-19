from django.contrib import admin
from .models import StudentProfile, Education, Skill, Project

admin.site.register(StudentProfile)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Project)