from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from shop.models import Product, SizeProduct, PhotoAlbum, Specifications, Services, Customer, Order
from shop.forms import ServicesForm, MakingOrderForm, FeedbackForm, QuestionForm
from django.http import JsonResponse
from shop.utils import get_client_ip, feedback_message, send_mail_with_order, get_queryset_to_dict, get_user


def ordering_feedback(request):
    if request.method == 'POST':
        if request.POST.get('checked'):
            form = FeedbackForm(request.POST)
        else:
            form = QuestionForm(request.POST)
        if form.is_valid():
            feedback_message(form.cleaned_data)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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

    def clear_basket(self):
        user = self.get_user()
        services = Services.objects.filter(customer=user)
        for i in services:
            i.delete()
        user.delete()

    def get(self, request):
        form = MakingOrderForm(initial={'payment_method': Order.IN_CASH, 'delivery_option': Order.DELIVERY})
        feedback_form = FeedbackForm()
        context = {
            'title_html': 'Оформление заказа',
            'form': form,
            'feedback_form': feedback_form,
            'user': get_user(request),
        }
        return render(request, 'shop/order.html', context=context)

    def post(self, request):
        form = MakingOrderForm(request.POST)
        if form.is_valid():
            form.save()
            services = self.get_services()
            mail = send_mail_with_order(services, form.cleaned_data)
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
        context['feedback_form'] = FeedbackForm()
        context['question_form'] = QuestionForm()
        context['user'] = get_user(self.request)
        return context

    def get_queryset(self):
        return Product.objects.filter(is_published=True)[:4]


class ShowAll(View):
    def get(self, request):
        count_post = request.GET.get('postCount')
        if int(count_post) > 4:
            queryset = Product.objects.filter(is_published=True)[:4]
        else:
            queryset = Product.objects.filter(is_published=True)
        data = get_queryset_to_dict(queryset)
        return JsonResponse({'data': data})


class Basket(ListView):
    model = Product
    template_name = 'shop/basket.html'
    context_object_name = 'prod'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_html'] = 'Корзина'
        context['feedback_form'] = FeedbackForm()
        context['user'] = get_user(self.request)
        products_shopping_cart = self.get_services()
        if not products_shopping_cart[0]:
            context['prod_list'] = None
        else:
            context['prod_list'] = products_shopping_cart[0]
            context['full_price'] = products_shopping_cart[1]
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
        context['feedback_form'] = FeedbackForm()
        context['user'] = get_user(self.request)
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
