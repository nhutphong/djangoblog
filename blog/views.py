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
from utils.decorators import record_terminal

class PaginationListView(ListView):
    model = Article
    template_name = 'articles/pagination_list.html'
    # queryset = Article.objects.all()
    paginate_by = 5

    @record_terminal("PaginationListView.get_queryset")
    def get_queryset(self):
        print("Tao la PaginationListView.get_queryset(self)")

        queryset = super().get_queryset()
        return queryset[::-1]
        # return Article.objects.all()[::-1]


class ArticleListView(ListView):
    # cac attrs class co nhieu methods tuong ung de thuc hien nhieu logic hon
    # queryset <=> get_context_data(self)

    model = Article
    template_name = 'articles/article_list.html'
    # context_object_name = 'article_list' # or object_list
    # queryset = Article.objects.all()  # <blog>/<modelname>_list.html

    @record_terminal('ArticleListView.get_queryset')
    def get_queryset(self): #run 1 -> end 1
        print("Tao la get_queryset(self)")

        queryset = super().get_queryset()
        return queryset[::-1]
        # return Article.objects.all()[::-1]

    # them logic dung ngoai template {{ today }}, {{ number }}
    @record_terminal('ArticleListView.get_context_data')
    def get_context_data(self, **kwargs): #run 2
        print("Tao la get_context_data(self, **kwargs)")
        print(f"{kwargs = }")

        # important
        context = super().get_context_data(**kwargs)
        print(f"{context = }")

        context['today'] = timezone.now()
        context['auto_number'] = random.randrange(1, 100)
        return context


    @record_terminal('ArticleListView.get_context_object_name')
    def get_context_object_name(self, object_list): #run 2.1
        print(f"{object_list = }")
        return "article_list" # end 2.1 -> end 2
        # return f"{type(object_list[0]).__name__.lower()}_list"
        


# @method_decorator(login_required, name='dispatch')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    # yeu cau dang nhap moi run dc ArticleCreateView
    # thua ke tu LoginRequiredMixin
    # login_url = '/accounts/login/'
    # redirect_field_name = 'next'

    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm
    #success_url = '/'


    def form_valid(self, form):
        print(f"ArticleCreateView.form_valid(self): form.cleaned_data: {form.cleaned_data}")

        #update article author is current user logged
        form.instance.author = self.request.user

        return super().form_valid(form)

    # def get_success_url(self):
    #    return '/'

    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article' # dung ngoai template {{ article }}
    query_pk_and_slug = True

    @record_terminal("ArticleDetailView.get_object")
    def get_object(self):
        slug = self.kwargs.get("slug")
        print("Tao la get_object(self)")
        print(f"self.kwargs: {self.kwargs}")
        return get_object_or_404(self.model, slug=slug)


# dung cho class base view
# @method_decorator(login_required, name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    # login_url = '/accounts/login/'
    # redirect_field_name = 'next'
    model = Article
    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm
    query_pk_and_slug = True

    @record_terminal("ArticleUpdateView.get_object")
    def get_object(self):
        print(f"Tao la get_object(self)")
        slug = self.kwargs.get("slug")
        # return get_object_or_404(Article, id=id_)
        return get_object_or_404(self.model, slug=slug)

    @record_terminal("ArticleUpdateView.form_valid")
    def form_valid(self, form):
        print("Tao la form_valid(self, form)")
        print(form.cleaned_data)
        return super().form_valid(form) # class FormMixin
        # 
        #return HttpResponseRedirect(self.get_success_url())
    
    #UserPassesTestMixin
    @record_terminal("ArticleUpdateView.test_func")
    def test_func(self):
        print("Tao la test_func(self)")
        article = self.get_object()
        return article.author == self.request.user
                                                                                                                                             
# yeu cau dang nhap moi run dc ArticleDeleteView
@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    # success_url = reverse_lazy('articles:article-list')
    query_pk_and_slug = True

    # raise_exception = True
    # permission_denied_message = "ban khong phai la owner"

    @record_terminal("ArticleDeleteView.get_object")
    def get_object(self):
        print("Tao la get_object(self)")
        slug = self.kwargs.get("slug")
        # return get_object_or_404(Article, id=id_)
        return get_object_or_404(self.model, slug=slug)

    @record_terminal("ArticleDeleteView.get_success_url")
    def get_success_url(self):
        print("Tao la get_success_url(self)")
        return reverse('articles:article-list')
    
    #UserPassesTestMixin
    @record_terminal("ArticleDeleteView.test_func")
    def test_func(self):
        print("Tao la test_func(self)")
        article = self.get_object()
        return article.author == self.request.user


class SearchResultsView(PaginationListView, ListView):
    
    model = Article
    template_name = 'articles/search_results.html'
    context_object_name = 'article_list'

    @record_terminal("SearchResultsView.get_queryset")
    def get_queryset(self):
        print("Tao la SearchResultsView START")
        query = self.request.GET.get('q')
        object_list = self.model.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )
        return object_list