from venv import create
from django.db import models
from main_auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(max_length=1000)
    author = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username + " - " +self.body[:20]

    class Meta:
        ordering = ["-created"]