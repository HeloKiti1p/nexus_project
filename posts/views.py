from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from .models import Post

def post_list(request):
    # Получаем все посты (уже отсортированы через Meta.ordering)
    posts = Post.objects.all()
    
    # Создаём объект пагинатора: по 5 постов на страницу
    paginator = Paginator(posts, 5)
    
    # Берём номер страницы из GET-параметра 'page', по умолчанию 1
    page_number = request.GET.get('page', 1)
    
    # Получаем объект текущей страницы (содержит посты и методы для навигации)
    page_obj = paginator.get_page(page_number)
    
    # Передаём в шаблон page_obj вместо posts
    return render(request, 'posts/post_list.html', {'page_obj': page_obj})