from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.utils.text import slugify

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=299
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='products',
        null=True
    )
    slug = models.SlugField(max_length=120, unique=True)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)  # default=True, null=True
    def __str__(self):
        return f"{self.title} {self.id}"

    # dung ngoai templates {{ obj.get_absolute_url }}
    def get_absolute_url(self):
        # f"/products/{self.id}/"
        return reverse("products:product-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
