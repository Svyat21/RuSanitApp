from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView
from shop.models import *


class ShopHome(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


class ShowProduct(DeleteView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = f'{context.product.name}'
        return context
