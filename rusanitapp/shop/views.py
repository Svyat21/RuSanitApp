from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
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


# class ShowProduct(DetailView):
#     model = Product
#     template_name = 'shop/product.html'
#     slug_url_kwarg = 'prod_slug'
#     context_object_name = 'prod'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_html'] = context['prod']
#         return context


# Изначально я пытался через клас отображать, потом подумал, что может что-то в классе не так провиса и
# сделал через функцию, но то же самое

def show_product(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)
    context = {
        'prod': prod,
        'title_html': prod.name,
    }
    return render(request, 'shop/product.html', context=context)
