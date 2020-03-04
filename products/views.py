from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProductForm
from .models import Product


def product_list_view(request):
    queryset = Product.objects.all()[::-1]  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "products/product_list.html", context)


def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
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
def product_update_view(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('products:product-list')
    context = {
        'form': form
    }
    return render(request, "products/product_create.html", context)


@login_required
def product_delete_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        return redirect('products:product-list')
    context = {
        "object": product
    }
    return render(request, "products/product_delete.html", context)