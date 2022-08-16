from django.contrib import admin
from .models import Post, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created',)
    list_filter = ('user',)


class CommentAdmin(admin.ModelAdmin):

    list_display = ('user', 'post', 'created', 'is_reply', 'reply')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

