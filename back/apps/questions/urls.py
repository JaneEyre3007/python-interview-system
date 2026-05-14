from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', QuestionViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
