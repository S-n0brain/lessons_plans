from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название предмета')

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ['name']

    def __str__(self):
        return self.name


class LessonType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип урока")

    class Meta:
        verbose_name = "Тип урока"
        verbose_name_plural = "Типы уроков"
        ordering = ['name']

    def __str__(self):
        return self.name


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
    name = models.CharField(max_length=10, unique=True, verbose_name="Класс")

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
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    subject_type = models.ForeignKey(to=LessonType, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="Тип урока")
    grade = models.ForeignKey(to=Grade, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Класс')
    topic = models.CharField(max_length=300, verbose_name="Тема")
    goal = models.TextField(blank=True, verbose_name="Цель")
    date_created = models.DateTimeField(auto_now_add=True)  # Дата добавления записи
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    plan_file = models.FileField(upload_to='lesson_plans/', verbose_name="Файл конспекта урока",
                                 null=True, blank=True)
    equipment = models.ManyToManyField(to=Equipment, null=True, blank=True,
                                       verbose_name="Оборудование")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['grade__name', 'subject__name']

    def __str__(self):
        grade = self.grade if self.grade.name else "Без класса"
        return f"{grade} — {self.subject.name} — {self.topic}"
