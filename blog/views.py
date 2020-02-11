import random
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils import timezone

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import ArticleModelForm
from .models import Article


class PaginationListView(ListView):
    template_name = 'articles/pagination_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.all()[::-1]


class ArticleListView(ListView):
    # cac attrs class co nhieu methods tuong ung de thuc hien nhieu login hon
    # queryset <=> get_context_data(self)

    template_name = 'articles/article_list.html'
    context_object_name = 'article_list'
    # queryset = Article.objects.all()  # <blog>/<modelname>_list.html

    def get_queryset(self):
        return Article.objects.all()[::-1]

    # them logic dung ngoai template {{ today }}, {{ number }}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['today'] = timezone.now()
        context['number'] = random.randrange(1, 100)
        return context


class ArticleDetailView(DetailView):
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    #queryset = Article.objects.all()
    query_pk_and_slug = True

    def get_object(self):
        slug = self.kwargs.get("slug")
        print(f"self.kwargs: {self.kwargs}")
        return get_object_or_404(Article, slug=slug)


# @method_decorator(login_required, name='dispatch')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    # yeu cau dang nhap moi run dc ArticleCreateView
    # thua ke tu LoginRequiredMixin
    # login_url = '/accounts/login/'
    # redirect_field_name = 'next'

    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()  # <blog>/<modelname>_list.html
    #success_url = '/'

    def form_valid(self, form):
        print(f"form.cleaned_data: {form.cleaned_data}")

        #form.instance.content = article.content
        #article.content = 'da changed from form_valid(self, form)'
        # form.instance.content = 'da changed from form_valid(self, form)'

        return super().form_valid(form)

    # def get_success_url(self):
    #    return '/'


# dung cho class base view
# @method_decorator(login_required, name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, UpdateView):

    # login_url = '/accounts/login/'
    # redirect_field_name = 'next'

    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


# yeu cau dang nhap moi run dc ArticleDeleteView
@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(DeleteView):
    template_name = 'articles/article_delete.html'
    # success_url = reverse_lazy('articles:article-list')

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def get_success_url(self):
        return reverse('articles:article-list')
