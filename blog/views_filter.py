import random
from django.shortcuts import render, get_object_or_404, redirect
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


def pair_attrs_request(request):
    request_attrs = {attr: getattr(request, attr) for attr in dir(request)}
    return request_attrs


def attrs_request(request):
    request_attrs = [getattr(request, attr) for attr in dir(request)]
    return request_attrs


def demo(request):
    template = 'blog/demo/demo_view.html'


    # print(f"{pair_attrs_request(request) = }")

    data = dict(name='thong', old=30, city='gia lai')
    iterable = ['cho', 'meo', 'heo', 'ga']
    pair_attrs = pair_attrs_request(request)
    attrs = range(1, 100)
    context = {
                'pair_attrs': pair_attrs,
                'attrs': attrs,
                'type': type(pair_attrs),
                'data': data,
                'iterable': iterable
            }


    return render(request, template, context)


def filter_test(request):
    template = 'blog/include/filters.html'
    full_name = 'nguyen chi thong'
    context = {
        'full_name': full_name
    }
    return render(request, template, context)