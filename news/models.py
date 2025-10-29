from django.db import models
from django.utils.text import slugify
from django.conf import settings

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    excerpt = models.TextField(max_length=400)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, default="Portage News Team")
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # If the user is deleted, keep the article but set creator to null
        null=True, blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(NewsArticle, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']