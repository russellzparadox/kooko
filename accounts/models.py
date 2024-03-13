import os

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    picture = models.ImageField(upload_to='media/user_pictures/', default='user_pictures/piri.png')
    email = models.EmailField(unique=True)
    description = models.TextField(null=True, blank=True)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.username


class Post(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/posts/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            # Rename the image to username_timestamp
            file_name, file_ext = os.path.splitext(os.path.basename(self.image.name))

            new_filename = f"{self.author.username}_{self.timestamp.strftime('%Y%m%d%H%M%S')}{file_ext}"
            self.image.name = new_filename
        super().save(*args, **kwargs)
