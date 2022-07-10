from django.urls import path
from .views import (
    product_create_view,
    product_detail_view,
    product_delete_view,
    product_list_view,
    product_update_view,

)

app_name = 'products'
urlpatterns = [
    # products/
    path('', product_list_view, name='product-list'),
    path('create/', product_create_view, name='product-create'),
    path('<slug:slug>/', product_detail_view, name='product-detail'),
    path('<slug:slug>/update/', product_update_view, name='product-update'),
    path('<slug:slug>/delete/', product_delete_view, name='product-delete'),
]
