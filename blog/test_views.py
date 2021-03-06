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


def get_all_attr_request(request):
    request_attrs = {attr: getattr(request, attr) for attr in dir(request)}
    return request_attrs


def home_test(request):
    template = 'articles/test/test_views.html'

    context = {'all': get_all_attr_request(request)}

    return render(request, template, context)


def filter_test(request):
    template = 'articles/include/filters.html'
    full_name = 'nguyen chi thong'
    context = {
        'full_name': full_name
    }
    return render(request, template, context)
