from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
 
from django.db.models.signals import(
	pre_save, post_save,
    post_delete,
)
from django.contrib.auth.signals import(
    user_logged_in,
    user_logged_out,
    user_login_failed
)
from django.core.signals import(
    request_started,
    request_finished
)
from django.dispatch import receiver

from utils.decorators import record_terminal


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(
        #verbose_name = 'article.content',
        blank=True,
        )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='articles', # user.articles
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
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f"{self.title[:10]} - {self.id}"

    # dung ngoai template, redirect cho CreateView
    @record_terminal("Article.get_absolute_url")
    def get_absolute_url(self):
        print(f"Tao la Article.get_absolute_url(self)")
        return reverse("articles:article-detail", kwargs={"slug": self.slug})

    @record_terminal("Article.save")
    def save(self, *args, **kwargs):  # new
        print(f"Tao la Article.save(self, *args, **kwargs)")
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        
    
    @property
    def picture_url(self):
        if self.picture:
            return self.picture.url
        return '#'

    def join_title_content(self):
        return self.title + ' ' + self.content

    def all_attrs(self):
        return {
            'title': self.title,
            'content': self.content,
            'active': self.active
        }

    # đinh nghĩa thêm nhiều methods() nhưng NOT arguments, sẽ dùng ngoài template như attributes
    # def one(self), def two(self), use template: article.one, article.two 



# signals = events
# pre: run dau save()
# post: run cuoi save()
# 


@receiver(pre_save, sender=Article) #cach 2
@record_terminal(name='pre_save', letter='+')
def pre_save_article(sender, instance, **kwargs):
	print(f"Tao la pre_save run khi article.save()")
    
#pre_save.connect(pre_save_article, sender=Article) cach 1
# pre_save_article() se run khi article = Article.objects.create(...,)
# or article.save()


@receiver(post_save, sender=Article)
@record_terminal(name='post_save', letter='+')
def post_save_article(sender, instance, created, **kwargs):
    print(f"1-sender: {sender} - 2-instance: {instance} - 3-created: {created}")
    print(f"post_save() run khi article.save() or Article.objects.create()")
#post_save.connect(post_save_article, sender=Article)


@receiver(post_delete, sender=Article)
@record_terminal(name='post_delete', letter='-')
def post_delete_article(sender, instance, using, **kwargs):
    print(f"1-sender: {sender} - 2-instance: {instance} - 3-using: {using}")
    print(
    	f"Tao la post_delete kich hoat khi run article.delete() 4-kwargs: {kwargs}"
    )


# run khi user da dang nhap
@receiver(user_logged_in)
@record_terminal(name='user_logged_in') #person
def user_login_receiver(sender, request, user, **kwargs):
    print(f"1-sender: {sender} - 2-request: {request} - 3-user: {user}")
    print(f"4-kwargs: {kwargs}")


@receiver(user_logged_out)
@record_terminal(name='user_logged_out') #person
def user_logout_receiver(sender, request, user, **kwargs):
    print(f"1-sender: {sender} - 2-request: {request} - 3-user: {user}")
    print(f"4-kwargs: {kwargs}")


@receiver(user_login_failed)
@record_terminal(name='user_login_failed') #person
def user_login_failed_receiver(sender, credentials, request, **kwargs):
    print(f"1-sender: {sender} - 2-credentials: {credentials} - 3-request: {request}")
    print(f"4-kwargs: {kwargs}")



# bat dau load page thi run
# @receiver(request_started)
# @record_terminal(name='request_started')
# def request_started_receiver(sender, environ, **kwargs):
#     print(f"sender: {sender} - environ: {environ} - kwargs: {kwargs}")


# khi load=f5 xong page se run
@receiver(request_finished)
@record_terminal(name='request_finished')
def request_finished_receiver(sender, **kwargs):
    print(f"1-sender: {sender} - 2-kwargs: {kwargs}")