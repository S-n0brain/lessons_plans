from django.apps import AppConfig


class LessonPlannerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lesson_planner'

    def ready(self):
        import lesson_planner.signals
