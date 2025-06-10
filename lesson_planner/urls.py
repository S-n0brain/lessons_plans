from django.urls import path
from .views import LessonPlanListView, LessonPlanDetailView

app_name = 'lesson_planner'

urlpatterns = [
    path('', LessonPlanListView.as_view(), name='index'),
    path('lesson/<int:pk>/', LessonPlanDetailView.as_view(), name='lesson_detail'),
    # path('lesson/<int:pk>/upload/', upload_lesson_plan_file, name='upload_lesson_plan')
]
