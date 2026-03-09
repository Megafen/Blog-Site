from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Like, Category
from .forms import CommentForm


def homepage(request):
    posts = Post.objects.all().order_by('-published_date')  # все статьи, сортировка от новых к старым
    return render(request, 'homepage/homepage.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None, active=True)  # только корневые активные комментарии
    comment_form = CommentForm()

    # Проверяем, ставил ли текущий пользователь лайк/дизлайк
    user_like = None
    if request.user.is_authenticated:
        like = Like.objects.filter(post=post, user=request.user).first()
        if like:
            user_like = like.value

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_like': user_like,
    }
    return render(request, 'homepage/post_detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).order_by('-published_date')
    return render(request, 'homepage/category_posts.html', {'category': category, 'posts': posts})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            comment.save()
            messages.success(request, 'Ваш комментарий добавлен и появится после проверки.' if not comment.active else 'Комментарий добавлен.')
    return redirect('post_detail', post_id=post.id)


@login_required
def like_post(request, post_id, action):
    post = get_object_or_404(Post, id=post_id)
    value = 1 if action == 'like' else -1  # лайк = 1, дизлайк = -1

    # Проверяем, есть ли уже оценка от этого пользователя
    like, created = Like.objects.get_or_create(post=post, user=request.user, defaults={'value': value})

    if not created:
        # Если оценка уже была
        if like.value == value:
            # Если нажали на ту же кнопку — удаляем оценку (отмена)
            like.delete()
            messages.info(request, 'Оценка убрана.')
        else:
            # Если нажали на противоположную — меняем значение
            like.value = value
            like.save()
            messages.success(request, 'Оценка изменена.')
    else:
        messages.success(request, 'Спасибо за оценку!')

    # Пересчитываем общее количество лайков и дизлайков для статьи
    post.total_likes = Like.objects.filter(post=post, value=1).count()
    post.total_dislikes = Like.objects.filter(post=post, value=-1).count()
    post.save()

    return redirect('post_detail', post_id=post.id)
