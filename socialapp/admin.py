from django.contrib import admin
from .models import Profile,Post,Comment,LikePost,Friends

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(Friends)