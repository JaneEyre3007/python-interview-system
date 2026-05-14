from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    avatar = models.URLField(blank=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserAIConfig(models.Model):
    PROVIDER_CHOICES = (
        ('openai', 'OpenAI兼容'),
        ('custom', '自定义'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_config', verbose_name='用户')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='openai', verbose_name='提供商')
    api_key = models.CharField(max_length=255, verbose_name='API Key')
    api_url = models.CharField(max_length=255, verbose_name='API地址')
    model_name = models.CharField(max_length=100, default='mimo-v2.5-pro', verbose_name='模型名称')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户AI配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} - {self.model_name}'
