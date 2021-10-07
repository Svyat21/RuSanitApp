from shop.models import Product, Services, Customer
from django.core.mail import send_mail


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def feedback_message(dict_message: dict):
    message = f"Заказан звонок от пользователя:\n{dict_message['name']}\n" \
              f"Номер телефона:\n{dict_message['phone']}\n"
    if dict_message.get('question'):
        message += f"Вопрос от пользователя:\n{dict_message['question']}"
    send_mail(
        subject=f"Заказ обратной связи от пользователя {dict_message['name']}",
        message=message,
        from_email='noreply@rs-eco.ru',
        recipient_list=['contact@rs-eco.ru'],
        fail_silently=False,
    )


def send_mail_with_order(services, order):
    order_prod, ful_price = services
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


def get_queryset_to_dict(queryset):
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


def get_count_prods(user, q_set):
    count = 0
    for obj in q_set:
        serv = Services.objects.filter(product=obj).filter(customer=user)
        if not serv:
            continue
        count += 1
    if count:
        return count
    return None


def get_user(request):
    ip = get_client_ip(request)
    user = Customer.objects.filter(user_ip=ip)
    if user:
        count_prod = Product.objects.filter(customer=user[0])
        if count_prod:
            return get_count_prods(user[0], count_prod)
    return None
