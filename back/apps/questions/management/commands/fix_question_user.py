from django.core.management.base import BaseCommand
from apps.questions.models import Question
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = '将所有 user=null 的题目分配给第一个管理员用户'

    def handle(self, *args, **options):
        null_questions = Question.objects.filter(user__isnull=True)
        if not null_questions.exists():
            self.stdout.write(self.style.SUCCESS('没有需要修复的题目'))
            return

        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            admin = User.objects.first()

        if not admin:
            self.stdout.write(self.style.ERROR('系统中没有用户'))
            return

        count = null_questions.update(user=admin)
        self.stdout.write(self.style.SUCCESS(f'已将 {count} 道题目分配给用户 {admin.username}'))
