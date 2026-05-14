from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/questions/', include('apps.questions.urls')),
    path('api/exams/', include('apps.exams.urls')),
    path('api/ai/', include('apps.ai.urls')),
]
