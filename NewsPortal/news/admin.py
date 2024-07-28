from django.contrib import admin
from .models import Post, Category, Author
from django.contrib.auth.models import User


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('title', 'category__name', 'author')
    search_fields = ('title', 'category__name', 'author__user__username')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'rating')
    list_filter = ('user_id__username', 'rating')
    search_fields = ('user_id__username', 'rating')


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)