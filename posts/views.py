from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.db.models import Count, Exists, OuterRef, Value, BooleanField
from .models import Post, Like
from .forms import PostForm

def post_list(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        posts = posts.annotate(
            liked_by_user=Exists(
                Like.objects.filter(post=OuterRef('pk'), user=request.user)
            )
        )
    else:
        posts = posts.annotate(liked_by_user=Value(False, output_field=BooleanField()))

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {'page_obj': page_obj})

def load_posts(request):
    page = request.GET.get('page')
    if not page:
        return HttpResponseBadRequest('Missing page parameter')

    posts = Post.objects.all()
    if request.user.is_authenticated:
        posts = posts.annotate(
            liked_by_user=Exists(
                Like.objects.filter(post=OuterRef('pk'), user=request.user)
            )
        )
    else:
        posts = posts.annotate(liked_by_user=Value(False, output_field=BooleanField()))

    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)

    html = render_to_string('posts/post_list_items.html', {'page_obj': page_obj, 'request': request})

    return JsonResponse({
        'html': html,
        'has_next': page_obj.has_next()
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
    return JsonResponse({
        'liked': liked,
        'total_likes': post.likes.count()
    })