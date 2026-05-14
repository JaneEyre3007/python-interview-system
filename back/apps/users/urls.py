from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserAIConfigView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('ai-config/', UserAIConfigView.as_view(), name='ai-config'),
]
