from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from shop.models import Product, SizeProduct, PhotoAlbum, Specifications, Services, Customer
from shop.forms import ServicesForm, MakingOrderForm
from django.core.mail import send_mail
from django.core import serializers
from django.http import JsonResponse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ordering_feedback(request):
    if request.GET:
        if request.GET['name'] and request.GET['phone']:
            mail = send_mail(
                subject=f"Заказ обратной связи от пользователя {request.GET['name']}",
                message=f"Заказан звонок от пользователя:\n{request.GET['name']}\n"
                        f"Номер телефона:\n{request.GET['phone']}",
                from_email='noreply@rs-eco.ru',
                recipient_list=['contact@rs-eco.ru'],
                fail_silently=False,
            )
            if mail:
                messages.success(request, 'Заявка отправлена!')
                return HttpResponse('ok', content_type='text/html')
            messages.error(request, 'Ошибка отправки!')
            return HttpResponse('no', content_type='text/html')
        messages.error(request, 'не все поля заполнены!')
        return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def remove_obj_basket(request, service_pk):
    obj = get_object_or_404(Services, pk=service_pk)
    obj.delete()
    return redirect('basket')


class MakingOrder(View):
    def get_user(self):
        ip = get_client_ip(self.request)
        user = Customer.objects.filter(user_ip=ip)
        if user:
            return user[0]
        else:
            return Customer.objects.create(user_ip=ip)

    def get_queryset(self):
        user = self.get_user()
        prod = Product.objects.filter(customer=user.pk)
        return prod

    def get_obj_price(self, obj):
        if obj.count == 0:
            return 0
        price = (obj.size.price + obj.montage.price + obj.elongated_neck.price +
                 obj.mounting_neck.price + obj.water_disposal.price +
                 obj.additional_options.price) * obj.count
        return price

    def get_services(self):
        user = self.get_user()
        object_list = self.get_queryset()
        full_price = 0
        q_set = []
        for obj in object_list:
            serv = Services.objects.filter(product=obj).filter(customer=user)
            if not serv:
                continue
            obj_price = self.get_obj_price(serv[0])
            full_price += obj_price
            q_set.append((obj, serv[0], obj_price))
        return q_set, full_price

    def send_mail_with_order(self, order):
        order_prod, ful_price = self.get_services()
        order_list = []
        order_data = ''
        for object in order_prod:
            prod = f"{object[0].name}\n" \
                   f"{object[1].count} шт. - {object[2]} руб.\n" \
                   f"Размер: {object[1].size}\n" \
                   f"Монтаж: {object[1].montage}\n" \
                   f"Удлиняющая горловина: {object[1].elongated_neck}\n" \
                   f"Монтаж горловины: {object[1].mounting_neck}\n" \
                   f"Водоотведение: {object[1].water_disposal}\n" \
                   f"Дополнительные опции: {object[1].additional_options}\n\n"
            order_list.append(prod)
        for i in order_list:
            order_data += i
        content_mail = f"Заявка на заказ от клиента:\n" \
                       f"Получатель: {order['recipient']}\n" \
                       f"Телефон: {order['phone_number']}\n" \
                       f"Email: {order['email']}\n" \
                       f"Город: {order['city']}. Улица: {order['street']}\n" \
                       f"Дом: {order['house_number']}. Квартира: {order['flat']}\n" \
                       f"Комментарий: {order['comment']}.\n" \
                       f"Оплата: {order['payment_method']}. Тип доставки: {order['delivery_option']}\n\n" \
                       f"Заказ на сумму - {ful_price} руб.:\n" + order_data
        mail = send_mail(
            subject=f"Заявка на заказ",
            message=content_mail,
            from_email='noreply@rs-eco.ru',
            recipient_list=['contact@rs-eco.ru'],
            fail_silently=False,
        )
        return mail

    def clear_basket(self):
        user = self.get_user()
        services = Services.objects.filter(customer=user)
        for i in services:
            i.delete()
        user.delete()

    def get(self, request):
        form = MakingOrderForm()
        context = {
            'title_html': 'Оформление заказа',
            'form': form,
        }
        return render(request, 'shop/order.html', context=context)

    def post(self, request):
        form = MakingOrderForm(request.POST)
        if form.is_valid():
            form.save()
            mail = self.send_mail_with_order(form.cleaned_data)
            if mail:
                self.clear_basket()
        return redirect('home')


class ShopHome(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = 'Главная страница'
        context['user'] = self.get_user()
        return context

    def get_queryset(self):
        return Product.objects.filter(is_published=True)[:4]

    def get_count_prods(self, user, q_set):
        count = 0
        for obj in q_set:
            serv = Services.objects.filter(product=obj).filter(customer=user)
            if not serv:
                continue
            count += 1
        if count:
            return count
        return None

    def get_user(self):
        ip = get_client_ip(self.request)
        user = Customer.objects.filter(user_ip=ip)
        if user:
            count_prod = Product.objects.filter(customer=user[0])
            print(f'\n{count_prod}\n')
            if count_prod:
                return self.get_count_prods(user[0], count_prod)
        return None


class ShowAll(View):
    def get_queryset_to_dict(self, queryset):
        data = []
        for prod in queryset:
            obj = {}
            if prod.tag_product:
                obj["tag_product"] = prod.tag_product
            else:
                obj["tag_product"] = None
            obj["people_amount"] = prod.specifications.people_amount
            obj["main_photo"] = prod.main_photo.url
            obj["name"] = prod.name
            obj["short_description"] = prod.short_description
            obj["get_absolute_url"] = prod.get_absolute_url()
            obj["price"] = prod.price
            data.append(obj)
        data.append({'count': queryset.count()})
        return data

    def get(self, request):
        count_post = request.GET.get('postCount')
        if int(count_post) > 4:
            queryset = Product.objects.filter(is_published=True)[:4]
        else:
            queryset = Product.objects.filter(is_published=True)
        data = self.get_queryset_to_dict(queryset)
        return JsonResponse({'data': data})


class Basket(ListView):
    model = Product
    template_name = 'shop/basket.html'
    context_object_name = 'prod'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = 'Корзина'
        context['prod_list'] = self.get_services()[0]
        context['full_price'] = self.get_services()[1]
        return context

    def get_user(self):
        ip = get_client_ip(self.request)
        user = Customer.objects.filter(user_ip=ip)
        if user:
            return user[0]
        else:
            return Customer.objects.create(user_ip=ip)

    def get_queryset(self):
        user = self.get_user()
        prod = Product.objects.filter(customer=user.pk)
        return prod

    def get_obj_price(self, obj):
        if obj.count == 0:
            return 0
        price = (obj.size.price + obj.montage.price + obj.elongated_neck.price +
                 obj.mounting_neck.price + obj.water_disposal.price +
                 obj.additional_options.price) * obj.count
        return price

    def get_services(self):
        user = self.get_user()
        full_price = 0
        q_set = []
        for obj in self.object_list:
            serv = Services.objects.filter(product=obj).filter(customer=user)
            if not serv:
                continue
            obj_price = self.get_obj_price(serv[0])
            full_price += obj_price
            q_set.append((obj, serv[0], obj_price))
        return q_set, full_price


class ShowProduct(DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'prod'

    def get_sizes(self):
        obj = self.get_object()
        return SizeProduct.objects.filter(product=obj.pk)

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
        context['form'] = ServicesForm(sizes=self.get_sizes())
        context['albums'] = self.get_album()
        context['photo_one'] = self.get_album_one()
        context['specifications'] = self.get_specifications()
        return context

    def get_user(self, request):
        ip = get_client_ip(request)
        user = Customer.objects.filter(user_ip=ip)
        if user:
            return user[0]
        else:
            return Customer.objects.create(user_ip=ip)

    def get_services(self, prod, user):
        service = Services.objects.filter(product=prod).filter(customer=user)
        if service:
            return service[0]
        return Services()

    def post(self, request, **kwargs):
        user = self.get_user(request)
        product = Product.objects.get(slug=kwargs['prod_slug'])
        service = self.get_services(product, user)

        sizes = self.get_sizes()
        form = ServicesForm(request.POST, sizes=sizes)
        if form.is_valid():
            service.size = form.cleaned_data['size']
            service.montage = form.cleaned_data['montage']
            service.elongated_neck = form.cleaned_data['elongated_neck']
            service.mounting_neck = form.cleaned_data['mounting_neck']
            service.water_disposal = form.cleaned_data['water_disposal']
            service.additional_options = form.cleaned_data['additional_options']
            service.count = form.cleaned_data['count']
            service.product = product
            service.customer = user
            service.save()
            product.customer = user
            product.save()
        return redirect('basket')