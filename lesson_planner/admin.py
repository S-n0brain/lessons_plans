from django.contrib import admin
from .models import Subject, LessonType, Teacher, Grade, Equipment, LessonPlan

admin.site.register(Subject)
admin.site.register(LessonType)
admin.site.register(Teacher)
admin.site.register(Grade)
admin.site.register(Equipment)
admin.site.register(LessonPlan)
