from django.db import models
from django.contrib.auth.models import User

class Content_Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_title = models.CharField(max_length=100)
    youtube_link = models.CharField(max_length=1000)
    blog_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.youtube_title

# Create your models here.
