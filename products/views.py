from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm
from .models import Product

from blog.utils import design


# def permission_of_user_for_posts(request,**kwargs):
#     product = get_object_or_404(Product, slug=request.GET.get('slug'))
#     if request.user.username == product.author:
#         return True
#     return False

@design("product_list_view")
def product_list_view(request):
    print("Tao la product_list_view(request)")
    template = "products/product_list.html"
    queryset = Product.objects.all()[::-1]  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, template, context)

@design("product_detail_view")
def product_detail_view(request, slug):
    print("Tao la product_detail_view(request, slug)")
    template = "products/product_detail.html"
    product = get_object_or_404(Product, slug=slug)
    context = {
        "object": product
    }
    return render(request, template, context)

@design("product_create_view")
def product_create_view(request):
    print('Tao la product_create_view(request)')
    template = "products/product_create.html"
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('products:product-list')
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
# @user_passes_test(permission_of_user_for_posts)
@design("product_update_view")
def product_update_view(request, slug):
    print("Tao la product_update_view(request, slug)")
    template = "products/product_create.html"
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('products:product-list')
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
# @user_passes_test(permission_of_user_for_posts)
@design("product_delete_view")
def product_delete_view(request, slug):
    print('Tao la product_delete_view(request, slug)')
    template = "products/product_delete.html"
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.delete()
        return redirect('products:product-list')
    context = {
        "object": product
    }
    return render(request, template, context)