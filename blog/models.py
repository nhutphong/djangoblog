from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
 
from django.db.models.signals import(
	pre_save, post_save,
    pre_delete, post_delete,
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
    def save(self, *args, **kwargs):  # overwrite
        print(f"Tao la Article.save(self, *args, **kwargs)")
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @record_terminal("Article.delete")
    def delete(self, *args, **kwargs):  # overwrite
        print(f"Tao la Article.delete(self, *args, **kwargs)")

        return super().delete(*args, **kwargs)
        
    
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

    # đinh nghĩa thêm nhiều methods() nhưng NOT arguments, sẽ dùng ngoài template như attributes == computed
    # def one(self), def two(self), use template: article.one, article.two 



# signals = lifecycle hook
# pre: run o dau in super().save(*args, **kwargs)
# post: run o cuoi in  super().save(*args, **kwargs)
# pre: run o dau in super().delete(*args, **kwargs)
# post: run o cuoi in  super().delete(*args, **kwargs)

# pre_init, post_init, m2m_changed


@receiver(pre_save, sender=Article) #cach 2
@record_terminal(name='pre_save', char='+')
def pre_save_article(sender, instance, **kwargs):
    print(f"Tao la pre_save run khi article.save()")
    print(f"sender: {sender}\ninstance: {instance}")
    print(f"kwargs {kwargs}")
    
#pre_save.connect(pre_save_article, sender=Article) cach 1
# pre_save_article() se run khi article = Article.objects.create(...,)
# or article.save()


@receiver(post_save, sender=Article)
@record_terminal(name='post_save', char='+')
def post_save_article(sender, instance, created, **kwargs):
    # create=True if la create article else create=False
    print(f"post_save() run khi article.save() or Article.objects.create()")
    print(f"sender: {sender}\ninstance: {instance}\ncreated: {created}")
    """
    if created: # create=True if create new article
        instance.title = 'set la title'
        instance.content = 'set lai content'
        # code them, nhung thu can vao block if nay
        instance.save() # se run lai pre_save vs post_save, nhung NOT run block if nua vi created=False
    """

#post_save.connect(post_save_article, sender=Article)


@receiver(pre_delete, sender=Article)
@record_terminal(name='pre_delete', char='-')
def pre_delete_article(sender, instance, using, **kwargs):
    print(
        f"Tao la pre_delete kich hoat khi run article.delete() or queryset.delete()"
    )
    print(f"sender: {sender}\ninstance: {instance}\nusing: {using}")
    print(f"kwargs: {kwargs}")


@receiver(post_delete, sender=Article)
@record_terminal(name='post_delete', char='-')
def post_delete_article(sender, instance, using, **kwargs):
    print(
    	f"Tao la post_delete kich hoat khi run article.delete() or queryset.delete()"
    )
    print(f"sender: {sender}\ninstance: {instance}\nusing: {using}")
    print(f"kwargs: {kwargs}")


# run khi user da dang nhap
@receiver(user_logged_in)
@record_terminal(name='user_logged_in') #person
def user_login_receiver(sender, request, user, **kwargs):
    print(f"sender: {sender}\nrequest: {request}\nuser: {user}")
    print(f"4-kwargs: {kwargs}")


@receiver(user_logged_out)
@record_terminal(name='user_logged_out') #person
def user_logout_receiver(sender, request, user, **kwargs):
    print(f"sender: {sender}\nrequest: {request}\nuser: {user}")
    print(f"4-kwargs: {kwargs}")


@receiver(user_login_failed)
@record_terminal(name='user_login_failed') #person
def user_login_failed_receiver(sender, credentials, request, **kwargs):
    print(f"sender: {sender}\ncredentials: {credentials}\nrequest: {request}\nkwargs: {kwargs}")



# bat dau load page thi run
# @receiver(request_started)
# @record_terminal(name='request_started')
# def request_started_receiver(sender, environ, **kwargs):
#     print(f"sender: {sender}\nenviron: {environ}\nkwargs: {kwargs}")


# khi load=f5 xong page se run
@receiver(request_finished)
@record_terminal(name='request_finished')
def request_finished_receiver(sender, **kwargs):
    print(f"sender: {sender}\nkwargs: {kwargs}")


"""
# nuoc sot
class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)


from django.dispatch import receiver
from django.db.models.signals import m2m_changed

@receiver(m2m_changed, sender=Pizza.toppings.through)
#Pizza.toppings.through = 
def toppings_changed(sender, **kwargs):
    # Do something
    pass
#m2m_changed.connect(toppings_changed, sender=Pizza.toppings.through)

>>> p = Pizza.objects.create(...)
>>> t = Topping.objects.create(...)
>>> p.toppings.add(t) #run toppings_changed()

sender      Pizza.toppings.through (the intermediate m2m class)
instance    p (the Pizza instance being modified)
action      "pre_add" (followed by a separate signal with "post_add")
reverse     False (Pizza contains the ManyToManyField, so this call modifies the forward relation)
model       Topping (the class of the objects added to the Pizza)
pk_set      {t.id} (since only Topping t was added to the relation)
using       "default" (since the default router sends writes here)


>>> t.pizza_set.remove(p) reverse
sender      Pizza.toppings.through (the intermediate m2m class)
instance    t (the Topping instance being modified)
action      "pre_remove" (followed by a separate signal with "post_remove")
reverse     True (Pizza contains the ManyToManyField, so this call modifies the reverse relation)
model       Pizza (the class of the objects removed from the Topping)
pk_set      {p.id} (since only Pizza p was removed from the relation)
using       "default" (since the default router sends writes here)


aciton in ['pre_add', 'post_add', 'pre_remove', 'post_remove', 'pre_clear', 'post_clear']


from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class Category(models.Model):
    pass

class Video(models.Model):
    categories = models.ManyToManyField(Category, related_name='videos')

@receiver(m2m_changed, sender=Video.categories.through)
def video_category_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    pk_set = kwargs.pop('pk_set', None)
    action = kwargs.pop('action', None)
    if action == "pre_add":
        if 1 not in pk_set:
            c = Category.objects.get(pk=1)
            instance.categories.add(c)
            instance.save()

video = Video.objects.create(...)
category = Catetory.objects.create(...)

video.categories.add(category) #run video_category_changed()
    instance = video
    reverse = False

    model = Catetory class
    pk_set = {category.id} # class set()


#reverse
category.videos.add(v) #run video_category_changed()
    instance = category
    reverse = True

    model = Video class
    pk_set = {video.id}
"""