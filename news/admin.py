from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'views_count', 'is_published',)
    list_filter = ('title', 'views_count', 'is_published',)
    search_fields = ('title', 'content',)
