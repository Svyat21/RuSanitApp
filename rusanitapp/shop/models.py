from django.db import models
from django.urls import reverse


product_tag = [
    ('Хит продаж', 'Хит продаж'),
    ('Новинка', 'Новинка'),
]

pay_method = [
    ('Наличными', 'Оплата наличными'),
    ('Переводом', 'Денежным переводом'),
]

reception_method = [
    ('Доставка', 'Доставка заказа до места получения'),
    ('Самовывоз', 'Самовывоз кастамаровский 3стр4'),
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
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('show_product', kwargs={'prod_slug': self.slug})

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'


class SizeProduct(models.Model):
    size = models.CharField(max_length=255, verbose_name='Размер')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Станция')

    class Meta:
        verbose_name = 'Размеры станции'
        verbose_name_plural = 'Размеры станции'


# class Customer(models.Model):
#     recipient = models.CharField(max_length=255, verbose_name='Получатель')
#     phone_number = models.CharField(max_length=255, verbose_name='Телефон')
#     email = models.CharField(max_length=255, verbose_name='email')
#     city = models.CharField(max_length=255, verbose_name='Город')
#     street = models.CharField(max_length=255, verbose_name='Улица')
#     house_number = models.CharField(max_length=255, verbose_name='Дом')
#     flat = models.CharField(max_length=255, verbose_name='Квартира')
#     comment = models.TextField(blank=True, verbose_name='Комментарий')
#     payment_method = models.CharField(max_length=255, choices=pay_method, verbose_name='Способ оплаты')
#     delivery_option = models.CharField(max_length=255, choices=reception_method, verbose_name='Вариант доставки')
#     product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.SET_NULL)


class Services(models.Model):
    size = models.CharField(max_length=255, default='Не выбрано', verbose_name='Размер')
    montage = models.BooleanField(default=False, verbose_name='Монтаж')
    elongated_neck = models.CharField(max_length=255, default='Не выбрано', verbose_name='Удлиняющая горловина')
    mounting_neck = models.BooleanField(default=False, verbose_name='Монтаж горловины')
    water_disposal = models.BooleanField(default=False, verbose_name='Водоотведение')
    additional_options = models.CharField(max_length=255, default='Не выбрано', verbose_name='Дополнительные опции')
    count = models.IntegerField(default=0, verbose_name='Количество в заказе')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'


class Specifications(models.Model):
    dimensions = models.CharField(max_length=255, verbose_name='Габариты')
    station_height = models.CharField(max_length=255, verbose_name='Высота корпуса станции')
    station_weight = models.CharField(max_length=255, verbose_name='Вес станции')
    people_amount = models.CharField(max_length=255, verbose_name='Количество пользователей')
    maximum_reset = models.CharField(max_length=255, verbose_name='Максимальный залповый сброс')
    power = models.CharField(max_length=255, verbose_name='Потребляемая мощность')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    class Meta:
        verbose_name = 'Характеристики'
        verbose_name_plural = 'Характеристики'


class PhotoAlbum(models.Model):
    photo = models.ImageField(upload_to=f'photos/', verbose_name='Главное фото')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    product = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL, verbose_name='Станция')
