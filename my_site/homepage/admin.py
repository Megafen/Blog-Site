from django.contrib import admin
from .models import Post, Comment, Like, Category


# Регистрируем категории
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}  # автоматически заполняет slug из названия
    list_editable = ('order',)  # позволяет менять порядок прямо в списке
    search_fields = ('name',)


# Обновляем PostAdmin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'total_likes', 'total_dislikes')
    list_filter = ('category', 'published_date')  # добавили фильтр по категориям
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'main_image', 'category', 'published_date', 'total_likes', 'total_dislikes')
    readonly_fields = ('total_likes', 'total_dislikes')  # запрещаем ручное редактирование счётчиков


# Остальные регистрации остаются без изменений
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('user__username', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Активировать выбранные комментарии"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value', 'created_at')
    list_filter = ('value',)
