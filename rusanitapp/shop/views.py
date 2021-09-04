from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from shop.models import Product, SizeProduct, PhotoAlbum, Specifications, Services, Customer
from shop.forms import ServicesForm
from django.core.mail import send_mail


def ordering_feedback(request):
    if request.GET:
        print(f'\nGET запрос обработан\n')
        print(f"\n{request.GET['name']}\n")
        print(f"\n{request.GET['phone']}\n")
        mail = send_mail(
            subject=f"Заказ обратной связи от пользователя {request.GET['name']}",
            message=f"Заказан звонок от пользователя:\n{request.GET['name']}\nНомер телефона:\n{request.GET['phone']}",
            from_email='noreply@rs-eco.ru',
            recipient_list=['contact@rs-eco.ru'],
            fail_silently=False,
        )
        if mail:
            messages.success(request, 'Заявка отправлена!')
            return HttpResponse('ok', content_type='text/html')
        else:
            messages.error(request, 'Ошибка отправки!')
            return HttpResponse('ok', content_type='text/html')
    else:
        print(f'\nGET запрос не обработан\n')
        return HttpResponse('no', content_type='text/html')


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


class Basket(ListView):
    model = Product
    template_name = 'shop/basket.html'
    context_object_name = 'prod'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = 'Корзина'
        context['prod_list'] = self.get_services()
        return context

    def get_user(self):
        ip = self.request.META.get('REMOTE_ADDR')
        user = Customer.objects.filter(user_ip=ip)
        if user:
            return user[0]
        else:
            return Customer.objects.create(user_ip=ip)

    def get_queryset(self):
        user = self.get_user()
        prod = Product.objects.filter(customer=user.pk)
        return prod

    def get_services(self):
        user = self.get_user()
        q_set = []
        for obj in self.object_list:
            serv = Services.objects.filter(product=obj).filter(customer=user)
            q_set.append((obj, serv[0]))
        return q_set


class ShowProduct(DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'prod'

    def get_sizes(self):
        obj = SizeProduct.objects.filter(product=self.object.pk)
        sizes = [(i.size, i.size) for i in obj]
        return sizes

    def get_album(self):
        obj = PhotoAlbum.objects.filter(product=self.object.pk)
        return obj

    def get_album_one(self):
        obj = PhotoAlbum.objects.filter(product=self.object.pk).first()
        return obj

    def get_specifications(self):
        obj = Specifications.objects.filter(product=self.object.pk)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = self.object.name
        sizes = self.get_sizes()
        context['form'] = ServicesForm(sizes=sizes)
        context['albums'] = self.get_album()
        context['photo_one'] = self.get_album_one()
        context['specifications'] = self.get_specifications()
        return context

    def get_user(self, request):
        ip = request.META.get('REMOTE_ADDR')
        user = Customer.objects.filter(user_ip=ip)
        if user:
            return user[0]
        else:
            return Customer.objects.create(user_ip=ip)

    def get_services(self, prod, user):
        service = Services.objects.filter(
            product=prod
        ).filter(customer=user)
        if service:
            return service[0]
        else:
            return Services()

    def post(self, request, **kwargs):
        user = self.get_user(request)
        product = Product.objects.get(slug=kwargs['prod_slug'])
        service = self.get_services(product, user)
        # sizes = self.get_sizes()
        # form = ServicesForm(request.POST, sizes=sizes)
        # if form.is_valid():
        service.size = request.POST['size']
        service.montage = request.POST['montage']
        service.elongated_neck = request.POST['elongated_neck']
        service.mounting_neck = request.POST['mounting_neck']
        service.water_disposal = request.POST['water_disposal']
        service.additional_options = request.POST['additional_options']
        service.count = request.POST['count']
        service.product = product
        service.customer = user
        service.save()
        product.customer = user
        product.save()
        return redirect('basket')


# class AddCart(View):
#     # template_name = 'shop/product.html'
#     def post(self, request, *args, **kwargs):
#         return HttpResponse('This is POST request')
