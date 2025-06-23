from django.contrib import admin
from .models import Work, Comment, Rating

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'published_date')
    list_filter = ('genre', 'published_date')
    search_fields = ('title', 'author__username', 'content')
    ordering = ('-published_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'work', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('text', 'user__username', 'work__title')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'work', 'score')
    list_filter = ('score',)
    search_fields = ('user__username', 'work__title')
