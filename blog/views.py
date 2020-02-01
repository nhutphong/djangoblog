import random
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils import timezone

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    ListView,
    DeleteView
)

from .forms import ArticleModelForm
from .models import Article


# @method_decorator(login_required, name='dispatch')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    #yeu cau dang nhap moi run dc ArticleCreateView
    #thua ke tu LoginRequiredMixin
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()  # <blog>/<modelname>_list.html
    #success_url = '/'

    def form_valid(self, form):
        print(form.cleaned_data)

        #form.instance.content = Article.content
        form.instance.content = 'da changed from form_valid(self, form)'
        print(form.cleaned_data)

        return super().form_valid(form)

    # def get_success_url(self):
    #    return '/'


class ArticleListView(ListView):
    # cac attrs class co nhieu methods tuong ung de thuc hien nhieu login hon
    # queryset <=> get_context_data(self)

    template_name = 'articles/article_list.html'
    # queryset = Article.objects.all()  # <blog>/<modelname>_list.html

    def get_queryset(self):
        return Article.objects.all()

    # them logic dung ngoai template {{ today }}, {{ number }}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['today'] = timezone.now()
        context['number'] = random.randrange(1, 100)
        return context


class ArticleDetailView(DetailView):
    template_name = 'articles/article_detail.html'
    #queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        print(f"self.kwargs: {self.kwargs}")
        return get_object_or_404(Article, id=id_)


# dung cho class base view
# @method_decorator(login_required, name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, UpdateView):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


#yeu cau dang nhap moi run dc ArticleDeleteView
@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(DeleteView):
    template_name = 'articles/article_delete.html'
    # success_url = reverse_lazy('articles:article-list')

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def get_success_url(self):
        return reverse('articles:article-list')