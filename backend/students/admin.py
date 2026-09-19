from django.contrib import admin
from .models import StudentProfile, Education, Skill

admin.site.register(StudentProfile)
admin.site.register(Education)
admin.site.register(Skill)