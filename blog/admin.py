from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)
    prepopulated_fields = {'slug': ('title',)}  # new


admin.site.register(Article, ArticleAdmin)
