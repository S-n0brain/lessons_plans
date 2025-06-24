from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название предмета',
                            help_text="Ведите название предмета")
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Автор")


    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ['name']

    def __str__(self):
        return self.name


class LessonType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип урока")
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Автор", blank=True, null=True)

    class Meta:
        verbose_name = "Тип урока"
        verbose_name_plural = "Типы уроков"
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class LessonStepTemplate(models.Model):
    lesson_type = models.ForeignKey(to=LessonType, on_delete=models.CASCADE, related_name="step_templates")
    name = models.CharField(max_length=200, verbose_name="Название этапа", help_text="Введите название этапа")
    order = models.PositiveIntegerField(verbose_name="Порядок", help_text="Введите порядковый номер этапа")
    object_step = models.Manager()
    DoesNotExist = models.Manager


    class Meta:
        verbose_name = "Этап шаблона"
        verbose_name_plural = "Этапы шаблонов"
        ordering = ['lesson_type', 'order']

    def __str__(self):
        return f"{self.lesson_type.name}: {self.order} {self.name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=70, null=True, blank=True,
                                  verbose_name="Отчество")
    subjects = models.ManyToManyField(to=Subject, verbose_name="Предметы")

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"
        ordering = ['last_name']

    def get_subjects(self):
        return ', '.join([x.name for x in self.subjects.all()])

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_subjects()})"


class Grade(models.Model):
    name = models.CharField(max_length=10, verbose_name="Класс")

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Оборудование")

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "оборудование"

    def __str__(self):
        return self.name


class LessonPlan(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='Предмет', help_text="Выберите предмет")
    subject_type = models.ForeignKey(to=LessonType, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="Тип урока", help_text="Выберите тип урока")
    grade = models.ForeignKey(to=Grade, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Класс', help_text="Выберите класс")
    topic = models.CharField(max_length=300, verbose_name="Тема", help_text="Введите тему урока")
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Автор")
    goal = models.TextField(blank=True, verbose_name="Цель", help_text="Введите цель урока")
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True, verbose_name="Дата обновления")
    plan_file = models.FileField(upload_to='lesson_plans/', verbose_name="Файл конспекта урока",
                                 null=True, blank=True)
    equipment = models.ManyToManyField(to=Equipment, null=True, blank=True, verbose_name="Оборудование", help_text="Выберите оборудование")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['grade__name', 'subject__name']

    def __str__(self):
        subject_type = self.subject_type.name if self.subject_type else "Без типа"
        grade = self.grade if self.grade.name else "Без класса"
        return f"{grade} - {self.subject.name} - {self.topic} - {subject_type}"

    def get_absolute_url(self):
        return reverse("lesson_planner:lesson_detail", args=[self.pk], current_app="lesson_planner")