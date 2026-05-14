from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', QuestionViewSet, basename='question')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
