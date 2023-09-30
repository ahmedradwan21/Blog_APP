from django.contrib import admin
from .models import BlogPost, UserProfile, Comment

admin.site.register(BlogPost)
admin.site.register(UserProfile)
admin.site.register(Comment)
