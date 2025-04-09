# app/blogs/admin.py
from django.contrib import admin
from .models import Category, BlogPost, Comment
from django.utils import timezone

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_at', 'created_at')
    list_filter = ('status', 'created_at', 'category', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    actions = ['publish_posts']
    
    def publish_posts(self, request, queryset):
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} posts were marked as published.')
    publish_posts.short_description = "Mark selected posts as published"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')