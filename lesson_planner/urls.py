from django.urls import path
from .views import LessonPlanListView

app_name = 'lesson_planner'

urlpatterns = [
    path('', LessonPlanListView.as_view(), name='index')
]
