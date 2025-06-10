from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LessonPlan
from .views import generate_plan_lesson_word

@receiver(signal=post_save, sender=LessonPlan)
def create_lesson_plan_docx(sender, instance, created, **kwargs):
    if created and instance.subject_type:
        generate_plan_lesson_word(lesson_plan=instance)


