from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('new/', views.post_create, name='create'),
    path('load_posts/', views.load_posts, name='load_posts'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]