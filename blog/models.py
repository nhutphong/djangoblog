from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.id}"

    # dung ngoai template, redirect cho CreateView
    def get_absolute_url(self):
        return reverse("articles:article-detail", kwargs={"id": self.id})

    def join_title_content(self):
        return self.title + ' ' + self.content

    def all_attrs(self):
        return {
            'title': self.title,
            'content': self.content,
            'active': self.active
        }
