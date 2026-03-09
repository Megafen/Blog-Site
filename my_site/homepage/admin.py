from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # какие поля показывать в списке
    list_display = ('title', 'published_date')
    list_filter = ('published_date',)           # фильтр по дате
    search_fields = ('title', 'content')        # поиск по заголовку и тексту
