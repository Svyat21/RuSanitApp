from django.http import HttpResponse
from django.shortcuts import render
from shop.models import *


def index(request):
    products = Product.objects.all()
    context = {
        'title_html': 'Главная страница',
        'title': 'Заголовок главной страницы',
        'products': products
    }
    return render(request, 'shop/index.html', context=context)


def product(request, prod_id):
    return HttpResponse(f'Конкретный продукт с номером id - {prod_id}.')
