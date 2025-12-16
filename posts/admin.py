from django.contrib import admin
from .models import Post, Comment, Like, Favourite, About, Author, Category, Tag


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)

try:
    admin.site.unregister(Post)
except:
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'timestamp', 'view_count']  # timestamp istifadə edildi
    readonly_fields = ['view_count']
    filter_horizontal = ['tags']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at', 'content']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title', 'content']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)