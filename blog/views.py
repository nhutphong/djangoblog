import random
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Q # new

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
        print("Tao la PaginationListView.get_queryset(self)")
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
        print("Tao la ArticleDetailView")
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
        print(f"ArticleCreateView.form_valid(self): form.cleaned_data: {form.cleaned_data}")

        #update article author is current user logged
        form.instance.author = self.request.user

        return super().form_valid(form)

    # def get_success_url(self):
    #    return '/'


# dung cho class base view
# @method_decorator(login_required, name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    # login_url = '/accounts/login/'
    # redirect_field_name = 'next'

    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm
    query_pk_and_slug = True

    def get_object(self):
        slug = self.kwargs.get("slug")
        # return get_object_or_404(Article, id=id_)
        return get_object_or_404(Article, slug=slug)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
    #UserPassesTestMixin
    def test_func(self):
        print("test_func(self)")
        obj = self.get_object()
        print(f"self.get_object(): {obj}")
        return obj.author == self.request.user
                                                                                                                                             
# yeu cau dang nhap moi run dc ArticleDeleteView
@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'articles/article_delete.html'
    # success_url = reverse_lazy('articles:article-list')
    query_pk_and_slug = True

    def get_object(self):
        slug = self.kwargs.get("slug")
        # return get_object_or_404(Article, id=id_)
        return get_object_or_404(Article, slug=slug)

    def get_success_url(self):
        return reverse('articles:article-list')
    
    #UserPassesTestMixin
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class SearchResultsView(PaginationListView, ListView):
    
    model = Article
    template_name = 'articles/search_results.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        print("Tao la SearchResultsView START")
        query = self.request.GET.get('q')
        object_list = Article.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )
        print(f"Tao la SearchResultsView END {self.request.GET.get}")
        return object_list
