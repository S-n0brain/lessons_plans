from django.contrib import admin
from .models import Subject, LessonType, Teacher, Grade, Equipment, LessonPlan, LessonStepTemplate

admin.site.register(Subject)
admin.site.register(LessonType)
admin.site.register(Teacher)
admin.site.register(Grade)
admin.site.register(Equipment)
admin.site.register(LessonStepTemplate)


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    fields = ["subject", "subject_type", "grade", "topic", "goal", "equipment"]
