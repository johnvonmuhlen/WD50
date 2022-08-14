import this
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follower(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="follows")
    followers = models.ManyToManyField(User, blank=True, related_name="following_usrs")
    followed_users = models.ManyToManyField(User, blank=True, related_name="followed_usrs")

class Post(models.Model):
    likes = models.IntegerField(max_length=999, default=0)
    total_comments = models.IntegerField(max_length=100, default=0)
    content = models.CharField(max_length=250, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post", default="user")

    def __str__(self):
        return f"{self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "likes": self.likes,
            "content": self.content,
            "user": self.user.username,
            "total_comments": self.total_comments,
        }