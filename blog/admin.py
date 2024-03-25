from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'views_count', 'is_published',)
    list_filter = ('title', 'views_count', 'is_published',)
    search_fields = ('title', 'content',)
