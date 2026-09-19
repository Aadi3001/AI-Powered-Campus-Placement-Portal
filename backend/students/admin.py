from django.contrib import admin
from .models import StudentProfile, Education, Skill, Project, Internship

admin.site.register(StudentProfile)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Internship)