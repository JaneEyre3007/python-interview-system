from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.questions'
    verbose_name = '题目管理'

    def ready(self):
        from .models import Question
        from django.contrib.auth import get_user_model
        User = get_user_model()

        null_count = Question.objects.filter(user__isnull=True).count()
        if null_count > 0:
            admin = User.objects.filter(is_superuser=True).first() or User.objects.first()
            if admin:
                Question.objects.filter(user__isnull=True).update(user=admin)
