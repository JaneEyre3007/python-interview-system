from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/questions/', include('apps.questions.urls')),
    path('api/exams/', include('apps.exams.urls')),
    path('api/ai/', include('apps.ai.urls')),
]
