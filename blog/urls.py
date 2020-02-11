from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    PaginationListView,
    ArticleListView,
    ArticleUpdateView,


)

app_name = 'articles'
urlpatterns = [
    path('pagination/', PaginationListView.as_view(), name='pagination-list'),
    path('', ArticleListView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path(
        '<int:id>/update/',
        ArticleUpdateView.as_view(),
        name='article-update'
    ),
    path(
        '<int:id>/delete/',
        ArticleDeleteView.as_view(),
        name='article-delete'
    ),
]
