from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(
        #verbose_name = 'article.content',
        blank=True,
        null=True

        )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='articles',
        null=True
    )
    picture = models.FileField(
        upload_to='pictures/%Y/%m/%d/',
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        )
    active = models.BooleanField(default=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f"{self.title} - {self.id}"

    # dung ngoai template, redirect cho CreateView
    def get_absolute_url(self):
        print(f"Tao la Article.get_absolute_url(self)")
        return reverse("articles:article-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def join_title_content(self):
        return self.title + ' ' + self.content

    def all_attrs(self):
        return {
            'title': self.title,
            'content': self.content,
            'active': self.active
        }
