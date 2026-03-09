from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # импортируем модель пользователя


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    # Добавим поля для подсчёта лайков и дизлайков (чтобы не вычислять каждый раз)
    total_likes = models.PositiveIntegerField(default=0, verbose_name='Всего лайков')
    total_dislikes = models.PositiveIntegerField(default=0, verbose_name='Всего дизлайков')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='Родительский комментарий')
    content = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    active = models.BooleanField(default=True, verbose_name='Активен')  # для модерации

    def __str__(self):
        return f'Комментарий {self.user.username} к {self.post.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']  # новые сверху


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1
    CHOICES = (
        (LIKE, 'Лайк'),
        (DISLIKE, 'Дизлайк'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    value = models.SmallIntegerField(choices=CHOICES, verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оценки')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('user', 'post')  # один пользователь — одна оценка на статью
