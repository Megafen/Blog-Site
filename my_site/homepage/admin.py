from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'total_likes', 'total_dislikes')
    list_filter = ('published_date',)
    search_fields = ('title', 'content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('user__username', 'content')
    actions = ['approve_comments']  # действие для массовой активации

    def approve_comments(self, request, queryset):
        queryset.update(active=True)  
    approve_comments.short_description = "Активировать выбранные комментарии"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value', 'created_at')
    list_filter = ('value',)
