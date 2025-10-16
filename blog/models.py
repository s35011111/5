from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview = models.ImageField(upload_to='blog/previews/', blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    
    def get_preview_url(self):
        if self.preview:
            return self.preview.url
        return '/static/blog/images/default-preview.jpg'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def increment_view_count(self):
        self.view_count += 1
        self.save()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['title']
