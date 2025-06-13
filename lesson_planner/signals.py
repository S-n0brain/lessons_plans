from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import LessonPlan
from django.db.models.fields.files import FieldFile
from .views import generate_plan_lesson_word
import os

# @receiver(signal=post_save, sender=LessonPlan)
# def create_lesson_plan_docx(sender, instance: LessonPlan, created, **kwargs):
#     if created and instance.subject_type:
#         generate_plan_lesson_word(lesson_plan=instance)


@receiver(signal=pre_delete, sender=LessonPlan)
def delete_lesson_plan_docx(sender, instance: LessonPlan, **kwargs):
    """
    Удаление файла плана урока при удалении объекта из бд
    """
    if instance.plan_file:
        instance.plan_file.delete(save=False)

@receiver(signal=pre_save, sender=LessonPlan)
def delete_old_file_docx_after_update(sender, instance: LessonPlan, **kwargs):
    """
    Удаление файла плана урока при замене на новый или при очистке старого плана
    """
    if not instance.pk:
        return

    old_file : FieldFile = LessonPlan.objects.get(pk=instance.pk).plan_file
    new_file : FieldFile = instance.plan_file
    print(new_file)
    print(old_file)
    if (old_file and not new_file) or (old_file and new_file):
        try:
            os.remove(path=old_file.path)
        except FileExistsError:
            return
