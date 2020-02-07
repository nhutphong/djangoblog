from django.db import models
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=3)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)  # default=True, null=True

    def __str__(self):
        return f"{self.title} {self.id}"

    #dung ngoai templates {{ obj.get_absolute_url }}
    def get_absolute_url(self):
        # f"/products/{self.id}/"
        return reverse("products:product-detail", kwargs={"id": self.id})
