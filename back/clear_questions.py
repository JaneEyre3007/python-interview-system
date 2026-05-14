import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.questions.models import Question, Category

count = Question.objects.count()
Question.objects.all().delete()
print(f'已删除 {count} 道题目')

Category.objects.all().delete()
print('已删除所有分类')
