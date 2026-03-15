from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def about(request):
    from django.http import HttpResponse
    return HttpResponse("Это моя социальная сеть! Скоро тут будет круто.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('', include('posts.urls')),          # главная лента
    path('', include('users.urls')),          # регистрация, логин и т.д.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)