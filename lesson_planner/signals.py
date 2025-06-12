from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import LessonPlan
from .views import generate_plan_lesson_word

# @receiver(signal=post_save, sender=LessonPlan)
# def create_lesson_plan_docx(sender, instance: LessonPlan, created, **kwargs):
#     if created and instance.subject_type:
#         generate_plan_lesson_word(lesson_plan=instance)


@receiver(signal=pre_delete, sender=LessonPlan)
def delete_lesson_plan_docx(sender, instance: LessonPlan, **kwargs):
    if instance.plan_file:
        instance.plan_file.delete(save=False)