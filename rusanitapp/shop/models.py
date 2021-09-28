from django.db import models
from django.urls import reverse


product_tag = [
    ('hit-of-sales', 'Хит продаж'),
    ('new-product', 'Новинка'),
]


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.IntegerField(verbose_name='Цена')
    short_description = models.CharField(max_length=255, verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание продукта')
    specifications = models.OneToOneField('Specifications', null=True, on_delete=models.SET_NULL)
    in_stock = models.IntegerField(verbose_name='остаток на стоке')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    main_photo = models.ImageField(upload_to='photos/', verbose_name='Главное фото')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    tag_product = models.CharField(max_length=255, blank=True, verbose_name='Тег', choices=product_tag)
    customer = models.ForeignKey('Customer', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='Не заполнять это поле', related_name='products')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('show_product', kwargs={'prod_slug': self.slug})

    def price_str(self):
        price_str = str(self.price)[::-1]
        res, last_el = '', 0
        for i in range(0, len(price_str), 3):
            res += price_str[i - 3:i] + ' '
            last_el = i
        res = res + price_str[last_el:]
        return res[::-1]

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'
        ordering = ['price']


class SizeProduct(models.Model):
    size = models.CharField(max_length=255, verbose_name='Размер')
    price = models.IntegerField(verbose_name='Цена')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Станция',
                                related_name='sizes_product')

    def __str__(self):
        return f'{self.size}: {self.price} руб.'

    class Meta:
        verbose_name = 'Размеры станции'
        verbose_name_plural = 'Размеры станции'
        ordering = ['product']


class Montage(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.name}: {self.price} руб.'

    class Meta:
        verbose_name = 'Монтаж'
        verbose_name_plural = 'Монтаж'


class ElongatedNeck(models.Model):
    size = models.CharField(max_length=255, verbose_name='Размер')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.size}: {self.price} руб.'

    class Meta:
        verbose_name = 'Удлиняющая горловина'
        verbose_name_plural = 'Удлиняющая горловина'


class MountingNeck(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.name}: {self.price} руб.'

    class Meta:
        verbose_name = 'Монтаж горловины'
        verbose_name_plural = 'Монтаж горловины'


class WaterDisposal(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.name}: {self.price} руб.'

    class Meta:
        verbose_name = 'Водоотведение'
        verbose_name_plural = 'Водоотведение'


class AdditionalOptions(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.name}: {self.price} руб.'

    class Meta:
        verbose_name = 'Дополнительные опции'
        verbose_name_plural = 'Дополнительные опции'


class Services(models.Model):
    size = models.ForeignKey('SizeProduct', blank=True, null=True, on_delete=models.SET_NULL)
    montage = models.ForeignKey('Montage', blank=True, null=True, on_delete=models.SET_NULL)
    elongated_neck = models.ForeignKey('ElongatedNeck', blank=True, null=True, on_delete=models.SET_NULL)
    mounting_neck = models.ForeignKey('MountingNeck', blank=True, null=True, on_delete=models.SET_NULL)
    water_disposal = models.ForeignKey('WaterDisposal', blank=True, null=True, on_delete=models.SET_NULL)
    additional_options = models.ForeignKey('AdditionalOptions', blank=True, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1, verbose_name='Количество в заказе')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, related_name='services')
    customer = models.ForeignKey('Customer', blank=True, null=True, on_delete=models.SET_NULL, related_name='services')

    def get_absolute_url(self):
        return reverse('basket_remove', kwargs={'service_pk': self.pk})

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'


class Customer(models.Model):
    user_ip = models.CharField(max_length=255, verbose_name='ip-адрес')
    order = models.OneToOneField('Order', null=True, on_delete=models.SET_NULL, related_name='customer')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Order(models.Model):
    IN_CASH = 'Наличными'
    MONEY_TRANSFER = 'Переводом'
    PAY_METHOD = [
        (IN_CASH, 'Оплата наличными'),
        (MONEY_TRANSFER, 'Денежным переводом'),
    ]
    DELIVERY = 'Доставка'
    PICKUP = 'Самовывоз'
    RECEPTION_METHOD = [
        (DELIVERY, 'Доставка заказа до места получения'),
        (PICKUP, 'Самовывоз'),
    ]
    recipient = models.CharField(max_length=255, verbose_name='Получатель')
    phone_number = models.CharField(max_length=255, verbose_name='Телефон')
    email = models.CharField(max_length=255, verbose_name='email')
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=255, verbose_name='Дом')
    flat = models.CharField(max_length=255, verbose_name='Квартира')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    payment_method = models.CharField(max_length=50, choices=PAY_METHOD, default=IN_CASH,
                                      verbose_name='Выберите способ оплаты')
    delivery_option = models.CharField(max_length=50, choices=RECEPTION_METHOD, default=DELIVERY,
                                       verbose_name='Выберите способ получения')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Specifications(models.Model):
    dimensions = models.CharField(max_length=255, verbose_name='Габариты')
    station_height = models.CharField(max_length=255, verbose_name='Высота корпуса станции')
    station_weight = models.CharField(max_length=255, verbose_name='Вес станции')
    people_amount = models.CharField(max_length=255, verbose_name='Количество пользователей')
    maximum_reset = models.CharField(max_length=255, verbose_name='Максимальный залповый сброс')
    power = models.CharField(max_length=255, verbose_name='Потребляемая мощность')

    class Meta:
        verbose_name = 'Характеристики'
        verbose_name_plural = 'Характеристики'


class PhotoAlbum(models.Model):
    photo = models.ImageField(upload_to=f'photos/', verbose_name='Главное фото')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    product = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL, verbose_name='Станция')

    class Meta:
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'
        ordering = ['product']
