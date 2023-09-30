# models.py in the 'blog' app
from django.db import models
from django.contrib.auth.models import User , Group

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_level = models.CharField(max_length=10, choices=[('viewer', 'Viewer'), ('writer', 'Writer'), ('admin', 'Admin')])
    groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)
    publish_status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
