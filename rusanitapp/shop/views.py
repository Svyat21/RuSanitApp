from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from shop.models import Product, SizeProduct, PhotoAlbum, Specifications
from shop.forms import ServicesForm


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


class ShowProduct(DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'prod'

    def get_form(self):
        obj = SizeProduct.objects.filter(product=self.object.pk)
        sizes = [(i.size, i.size) for i in obj]
        form = ServicesForm(sizes=sizes)
        return form

    def get_album(self):
        obj = PhotoAlbum.objects.filter(product=self.object.pk)
        return obj

    def get_album_one(self):
        obj = PhotoAlbum.objects.filter(product=self.object.pk).first()
        return obj

    def get_specifications(self):
        obj = Specifications.objects.filter(product=self.object.pk)
        print(obj)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = self.object.name
        context['form'] = self.get_form()
        context['albums'] = self.get_album()
        context['photo_one'] = self.get_album_one()
        context['specifications'] = self.get_specifications()
        return context


# def show_product(request, prod_slug):
#     prod = get_object_or_404(Product, slug=prod_slug)
#     context = {
#         'prod': prod,
#         'title_html': prod.name,
#     }
#     return render(request, 'shop/product.html', context=context)
