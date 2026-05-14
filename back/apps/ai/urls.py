from django.urls import path
from .views import GenerateQuestionView, EvaluateAnswerView, TokenUsageStatsView

urlpatterns = [
    path('generate/', GenerateQuestionView.as_view(), name='generate'),
    path('evaluate/', EvaluateAnswerView.as_view(), name='evaluate'),
    path('token-stats/', TokenUsageStatsView.as_view(), name='token-stats'),
]
