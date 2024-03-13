from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    picture = models.ImageField()
    # email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.username
