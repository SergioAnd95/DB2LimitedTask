from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_preview_text', 'date_created')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date_created')


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_created')