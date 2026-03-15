from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),   # сначала
    path('profile/<str:username>/', views.profile_view, name='profile'), # потом
]


