from django.db import models
from django.conf import settings


class TokenUsage(models.Model):
    API_TYPE_CHOICES = (
        ('generate', '生成题目'),
        ('evaluate', '评判答案'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户')
    api_type = models.CharField(max_length=20, choices=API_TYPE_CHOICES, verbose_name='API类型')
    prompt_tokens = models.IntegerField(default=0, verbose_name='输入Token')
    completion_tokens = models.IntegerField(default=0, verbose_name='输出Token')
    total_tokens = models.IntegerField(default=0, verbose_name='总Token')
    model_name = models.CharField(max_length=50, default='mimo-v2.5-pro', verbose_name='模型名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='调用时间')

    class Meta:
        verbose_name = 'Token消耗记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_api_type_display()} - {self.total_tokens} tokens'

    def save(self, *args, **kwargs):
        self.total_tokens = self.prompt_tokens + self.completion_tokens
        super().save(*args, **kwargs)
