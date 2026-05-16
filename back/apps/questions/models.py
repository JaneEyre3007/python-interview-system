from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '题目分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = (
        ('choice', '选择题'),
        ('fill', '填空题'),
        ('code', '编程题'),
        ('short', '简答题'),
    )

    DIFFICULTY_LEVELS = (
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='所属用户')
    bank_name = models.CharField(max_length=100, blank=True, verbose_name='题库名')
    is_published = models.BooleanField(default=False, verbose_name='已上线')
    type = models.CharField(max_length=10, choices=QUESTION_TYPES, verbose_name='题目类型')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium', verbose_name='难度')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='分类')
    content = models.TextField(verbose_name='题目内容')
    options = models.JSONField(default=dict, blank=True, verbose_name='选项（选择题）')
    answer = models.TextField(verbose_name='正确答案')
    explanation = models.TextField(blank=True, verbose_name='答案解析')
    created_by_ai = models.BooleanField(default=False, verbose_name='AI生成')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_type_display()}] {self.content[:50]}'
