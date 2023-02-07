from django.contrib import admin
from .models import Post, PostLike, CommentLike, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Comment)



