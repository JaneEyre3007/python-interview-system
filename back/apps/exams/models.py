from django.db import models
from django.conf import settings
from apps.questions.models import Question


class Exam(models.Model):
    STATUS_CHOICES = (
        ('pending', '待完成'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=200, verbose_name='试卷标题')
    questions = models.ManyToManyField(Question, through='ExamQuestion')
    total_score = models.IntegerField(default=0, verbose_name='总分')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.title}'


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name='序号')
    score = models.IntegerField(default=10, verbose_name='分值')

    class Meta:
        ordering = ['order']


class Answer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='answers', verbose_name='试卷')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='exam_answers', verbose_name='题目')
    user_answer = models.TextField(verbose_name='用户答案')
    is_correct = models.BooleanField(default=False, verbose_name='是否正确')
    score = models.IntegerField(default=0, verbose_name='得分')
    ai_feedback = models.TextField(blank=True, verbose_name='AI反馈')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='答题时间')

    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = verbose_name
        unique_together = ['exam', 'question']

    def __str__(self):
        return f'{self.exam.title} - {self.question.content[:20]}'
