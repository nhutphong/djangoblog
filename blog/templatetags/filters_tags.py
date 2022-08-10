from django import template

register = template.Library()


#template {{ value|split:"two" }}
#khong co param two cang tot
@register.filter
def my_split(value, two=None):
    return value.split(sep=two)


#template {% my_tag 2 3 9 1 3 2 name='phong' old=27 %}
@register.simple_tag
def my_simple_tag(a, b, *args, **kwargs):
    return [a,b, args, kwargs]


# {% my_inclusion_tag request %} #template call
@register.inclusion_tag('blog/include/inclusion_tag.html')
def my_inclusion_tag(request):
    user_articles = request.user.articles.all()
    return {'article_list': user_articles}