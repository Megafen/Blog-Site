from django.shortcuts import render, get_object_or_404
from .models import Post  # импортируем модель Post


def homepage(request):
    posts = Post.objects.all().order_by('-published_date')  # все статьи, сортировка от новых к старым
    return render(request, 'homepage/homepage.html', {'posts': posts})


def post_detail(request, post_id):
    # Получаем статью по id или возвращаем 404, если не найдена
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'homepage/post_detail.html', {'post': post})
