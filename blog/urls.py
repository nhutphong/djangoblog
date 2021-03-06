from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    ArticleListView,
    ArticleCreateView,
    
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,

    PaginationListView,
    SearchResultsView,
)
from . import test_views


app_name = 'articles'
urlpatterns = [

    #/blog/
    path('test/', test_views.home_test, name='test-home'),
    path('filter/', test_views.filter_test, name='filter-list'),
    path('pagination/', PaginationListView.as_view(), name='pagination-list'),
    path('timkiem/', SearchResultsView.as_view(), name='search-results'),

    path('', ArticleListView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),

    path(
        '<slug:slug>/update/',
        ArticleUpdateView.as_view(),
        name='article-update'
    ),

    path(
        '<slug:slug>/delete/',
        ArticleDeleteView.as_view(),
        name='article-delete'
    )
    
]