from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
 
from django.db.models.signals import post_save
from django.dispatch import receiver


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(
        #verbose_name = 'article.content',
        blank=True,
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
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, null=False, unique=True)

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


@receiver(post_save, sender=Article) #cach 2
def create_profile(sender, instance, created, **kwargs):
	print(f"sender: {sender} - instance: {instance} - created: {created} - kwargs:{kwargs}")
    # sender = class Article, instance = new_article

	# if created: 
	# 	Profile.objects.create(user=instance)
	# 	print('Profile created!')

#post_save.connectp(create_rofile, sender=Article) cach 1
# create_profile() se run khi article = Article.objects.create(...,)
# or article.save()


# @receiver(post_save, sender=Article)
# def update_profile(sender, instance, created, **kwargs):
	
# 	if created == False:
# 		instance.profile.save()
# 		print('Profile updated!')


#post_save.connect(update_profile, sender=User)