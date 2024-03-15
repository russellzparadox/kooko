import os
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    picture = models.ImageField(upload_to='media/user_pictures/', default='user_pictures/piri.png')
    email = models.EmailField(unique=True)
    description = models.TextField(null=True, blank=True)
    follows = models.ManyToManyField('accounts.User', related_name='followers')
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        # if self.pk is not None and self.picture:
        #     # Rename the image to username_timestamp
        #     file_name, file_ext = os.path.splitext(os.path.basename(self.picture.name))
        #     current_timestamp = datetime.now()
        #     timestamp_text = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        #
        #     new_filename = f"{self.username}_{timestamp_text}{file_ext}"
        #     self.picture.name = new_filename
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.username


class Post(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/posts/', blank=True, null=True)
    likeCount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is  None and self.image:
            # Rename the image to username_timestamp
            file_name, file_ext = os.path.splitext(os.path.basename(self.image.name))

            new_filename = f"{self.author.username}_{self.timestamp.strftime('%Y%m%d%H%M%S')}{file_ext}"
            self.image.name = new_filename
        super().save(*args, **kwargs)


class Comment(models.Model):
    body = models.TextField()
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
