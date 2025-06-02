from django.shortcuts import render
from django.views.generic import ListView
from .models import LessonPlan

class LessonPlanListView(ListView):
    model = LessonPlan
    template_name = "lesson_planner/index.html"
    extra_context = {"title": "Главная страница"}
    context_object_name = "lesson_plans"
