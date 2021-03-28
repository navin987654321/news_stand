from django.db import models
from django.utils.timezone import now

# Create your models here.

class Post(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(default=now)