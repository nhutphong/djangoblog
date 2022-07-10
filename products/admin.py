from django.contrib import admin
from .models import Product


@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
