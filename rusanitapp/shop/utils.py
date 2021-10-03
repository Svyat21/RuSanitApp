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
