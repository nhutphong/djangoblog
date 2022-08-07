from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    #list_display = ('title', 'content',)
    list_display = ('title', 'content_short',)

    prepopulated_fields = {'slug': ('title',)}  # new


    # view column content chi 100 chars
    @admin.display(description='content 100')
    def content_short(self, obj):
        return obj.content[:100] + '...'


admin.site.register(Article, ArticleAdmin)