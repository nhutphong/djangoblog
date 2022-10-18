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
    template_name = 'blog/pagination_list.html'
    # queryset = Article.objects.all()
    paginate_by = 5

    @record_terminal("PaginationListView.get_queryset")
    def get_queryset(self):
        print("Tao la PaginationListView.get_queryset(self)")

        queryset = super().get_queryset()
        return queryset[::-1]
        # return Article.objects.all()[::-1]


class ArticleListView(ListView):
    """ 
        inherit tu ListView
        # cac attrs class co nhieu methods tuong ung de thuc hien nhieu logic hon


        run 1, end 1
        ArticleListView.get_queryset(self)

        run 2
        ArticleListView.get_context_data(self, **kwargs):
           # important
            context = super().get_context_data(**kwargs):
                ArticleListView.get_context_object_name(self, object_list)
        end 2

        run 3, end 3 # class in file models.py
        Article.get_absolute_url(self)

        run 4, end 4
        request_fineshed()      #django signal

    """


    model = Article
    template_name = 'blog/article_list.html'
    # context_object_name = 'article_list' # default 'object_list'
    # queryset = Article.objects.all()  # <blog>/<modelname>_list.html

    @record_terminal('ArticleListView.get_queryset')
    def get_queryset(self): #run ONE -> end ONE
        print("Tao la get_queryset(self)")

        queryset = super().get_queryset()
        return queryset[::-1]
        # return Article.objects.all()[::-1]

    # them logic dung ngoai template {{ today }}, {{ number }}
    @record_terminal('ArticleListView.get_context_data')
    def get_context_data(self, **kwargs): #START TWO
        print("Tao la get_context_data(self, **kwargs)")
        print(f"{kwargs = }")

        # important
        context = super().get_context_data(**kwargs) # CALL THREE

        print(f"{context = }")

        context['today'] = timezone.now()
        context['auto_number'] = random.randrange(1, 100)
        return context #END TWO


    @record_terminal('ArticleListView.get_context_object_name', char='-')
    def get_context_object_name(self, object_list): #START THREE
        print(f"{object_list = }")
        return "article_list" # END THREE -> sau do (END TWO)
        # return f"{type(object_list[0]).__name__.lower()}_list"
        


# @method_decorator(login_required, name='dispatch')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    # yeu cau dang nhap moi run dc ArticleCreateView
    # thua ke tu LoginRequiredMixin
    # login_url = '/accounts/login/'
    # redirect_field_name = 'next'

    template_name = 'blog/article_create.html'
    form_class = ArticleModelForm
    #success_url = '/' # = get_success_url(self)


    def form_valid(self, form):
        print(f"ArticleCreateView.form_valid(self):\n\tform.cleaned_data: {form.cleaned_data}")

        #update article author is current user logged
        form.instance.author = self.request.user

        return super().form_valid(form)

    # def get_success_url(self):
    #    return '/'

    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
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
    template_name = 'blog/article_create.html'
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
        # user da login, cung phai la tac gia bai bao, moi duoc update
                                                                                                                                             
# yeu cau dang nhap moi run dc ArticleDeleteView
@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/article_delete.html'
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
        # user da login, cung phai la tac gia bai bao, moi duoc delete


class SearchResultsView(PaginationListView, ListView):
    
    model = Article
    template_name = 'blog/search_results.html'
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