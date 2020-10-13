from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import(
    login_required,
    user_passes_test,
    permission_required
)
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .forms import ProductModelForm
from .models import Product

from utils.decorators import record_terminal

def is_super(user, **kwargs):
    print(kwargs)
    return user.is_superuser

@record_terminal("product_list_view")
def product_list_view(request):
    print("Tao la product_list_view(request)")
    template = "products/product_list.html"
    queryset = Product.objects.all()[::-1]  # list of objects
    context = {
        "object_list": queryset
    }

    return render(request, template, context)


@login_required
@record_terminal("product_create_view")
def product_create_view(request):
    print('Tao la product_create_view(request)')
    template = "products/product_create.html"
    form = ProductModelForm(request.POST or None)

    if form.is_valid():
        product = form.save(commit=False)
        product.author = request.user
        product.save()

        return redirect('products:product-list')

    context = {
        'form': form
    }
    return render(request, template, context)


@record_terminal("product_detail_view")
def product_detail_view(request, slug):
    print("Tao la product_detail_view(request, slug)")
    
    template = "products/product_detail.html"
    product = get_object_or_404(Product, slug=slug)
    context = {
        "object": product
    }

    return render(request, template, context)


@login_required
@record_terminal("product_update_view")
def product_update_view(request, slug):
    print("Tao la product_update_view(request, slug)")
    template = "products/product_create.html"
    product = get_object_or_404(Product, slug=slug)
    form = ProductModelForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('products:product-list')

    context = {
        'form': form
    }

    return render(request, template, context)


# @user_passes_test(is_super, redirect_field_name='next')
# @permission_required("product.delete_view", raise_exception=True)
@record_terminal("product_delete_view")
def product_delete_view(request, slug):
    print('Tao la product_delete_view(request, slug)')
    # print(request.path)
    if not request.user.is_superuser:
        raise PermissionDenied
        # return redirect(f"/accounts/login/?next={request.path}")

    template = "products/product_delete.html"
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.delete()
        return redirect('products:product-list')

    context = {
        "object": product
    }
    
    return render(request, template, context)