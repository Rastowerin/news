from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    redacted = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


class New(Post):
    title = models.CharField(max_length=100, default='')
    creator = models.ForeignKey('auth.user', related_name='created_news', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Comment(Post):
    commented_new = models.ForeignKey(New, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:50]
