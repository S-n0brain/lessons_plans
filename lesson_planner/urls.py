from django.urls import path
from .views import (LessonPlanListView, LessonPlanDetailView, LessonPlanCreateView,
                    LessonPlanDeleteView, LessonPlanUpdateView,
                    SubjectListView, SubjectDeleteView, SubjectTypeListView,
                    SubjectTypeDeleteView, LessonStepTemplateListView, LessonStepTemplateDeleteView)

app_name = 'lesson_planner'

urlpatterns = [
    path('', LessonPlanListView.as_view(), name='index'),
    path('lesson/<int:pk>/', LessonPlanDetailView.as_view(), name='lesson_detail'),
    path('lesson/create/', LessonPlanCreateView.as_view(), name='create_lesson_plan'),
    path("lesson/<int:pk>/delete/", LessonPlanDeleteView.as_view(), name="delete_lesson"),
    path("lesson/<int:pk>/update/", LessonPlanUpdateView.as_view(), name="update_lesson"),
    path("subjects/", SubjectListView.as_view(), name="subjects_list"),
    path("subjects/<int:pk>/delete/", SubjectDeleteView.as_view(), name="delete_subject"),
    path("subject_types/", SubjectTypeListView.as_view(), name="subject_types_list"),
    path("subject_types/<int:pk>/delete/", SubjectTypeDeleteView.as_view(), name="delete_subject_type"),
    path("subject_steps/<int:pk>/", LessonStepTemplateListView.as_view(), name="lessons_steps_list"),
    path("subject_steps/<int:pk>/delete/", LessonStepTemplateDeleteView.as_view(), name="delete_step"),
]

