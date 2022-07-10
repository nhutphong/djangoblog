from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from utils.decorators import record_terminal


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)

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
    ) # request.user.products

    slug = models.SlugField(max_length=120, unique=True)
    summary = models.TextField()
    featured = models.BooleanField(default=False)  # default=True, null=True
    
    def __str__(self):
        return f"{self.title} {self.id}"

    # dung ngoai templates {{ obj.get_absolute_url }}
    @record_terminal("Product.get_absolute_url")
    def get_absolute_url(self):
        print("Tao la get_absolute_url(self)")
        # f"/products/{self.id}/"
        return reverse("products:product-detail", kwargs={"slug": self.slug})

    @record_terminal("Product.save")
    def save(self, *args, **kwargs):  # new
        print("Tao la save(self, *args, **kwargs)")
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)