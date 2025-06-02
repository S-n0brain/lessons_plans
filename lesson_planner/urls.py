from django.urls import path
from .views import index

app_name = 'lesson_planner'

urlpatterns = [
    path('', index, name='index')
]
