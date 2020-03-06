from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm
from .models import Product


# def permission_of_user_for_posts(request,**kwargs):
#     product = get_object_or_404(Product, slug=request.GET.get('slug'))
#     if request.user.username == product.author:
#         return True
#     return False


def product_list_view(request):
    queryset = Product.objects.all()[::-1]  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "products/product_list.html", context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        "object": product
    }
    return render(request, "products/product_detail.html", context)


def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('products:product-list')
    context = {
        'form': form
    }
    return render(request, "products/product_create.html", context)


@login_required
# @user_passes_test(permission_of_user_for_posts)
def product_update_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('products:product-list')
    context = {
        'form': form
    }
    return render(request, "products/product_create.html", context)


@login_required
# @user_passes_test(permission_of_user_for_posts)
def product_delete_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.delete()
        return redirect('products:product-list')
    context = {
        "object": product
    }
    return render(request, "products/product_delete.html", context)