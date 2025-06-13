from django.urls import path
from .views import LessonPlanListView, LessonPlanDetailView, LessonPlanCreateView, LessonPlanDeleteView, LessonPlanUpdateView

app_name = 'lesson_planner'

urlpatterns = [
    path('', LessonPlanListView.as_view(), name='index'),
    path('lesson/<int:pk>/', LessonPlanDetailView.as_view(), name='lesson_detail'),
    path('lesson/create/', LessonPlanCreateView.as_view(), name='create_lesson_plan'),
    path("lesson/<int:pk>/delete/", LessonPlanDeleteView.as_view(), name="delete_lesson"),
    path("lesson/<int:pk>/update/", LessonPlanUpdateView.as_view(), name="update_lesson")
]
