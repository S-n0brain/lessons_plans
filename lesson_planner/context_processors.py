from urllib.request import Request
from .models import LessonType, Subject
from django.db.models import QuerySet

def types_lessons(request: Request) -> dict[str, QuerySet]:
    return {'types_lessons': LessonType.objects.all()}

def subjects(request: Request) -> dict[str, QuerySet]:
    return {'subjects': Subject.objects.all()}