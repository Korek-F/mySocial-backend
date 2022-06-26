from django.db import models
from main_auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(max_length=1000)
    author = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked", blank=True)

    def __str__(self):
        return self.author.username + " - " +self.body[:20]

    class Meta:
        ordering = ["-created"]

class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comment_onwer", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_comments", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="comment_liked", blank=True)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="comment_child")

    class Meta:
        ordering = ["-created"]
        
    @property 
    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return str(self.pk) + " - " + self.author.username + " - " +self.content[:20]