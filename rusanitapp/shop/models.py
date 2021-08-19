from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.IntegerField(verbose_name='Цена')
    short_description = models.CharField(max_length=255, verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание продукта')
    specifications = models.OneToOneField('Specifications', null=True, on_delete=models.SET_NULL)
    services = models.OneToOneField('Services', null=True, on_delete=models.SET_NULL)
    in_stock = models.IntegerField(verbose_name='остаток на стоке')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    main_photo = models.ImageField(upload_to='photos/', verbose_name='Главное фото')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    count = models.IntegerField(verbose_name='Количество в заказе', null=True)
    # slug =

    def __str__(self):
        return f'{self.pk}. {self.name}'

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_id': self.pk})


class Customer(models.Model):
    recipient = models.CharField(max_length=255, verbose_name='Получатель')
    phone_number = models.CharField(max_length=255, verbose_name='Телефон')
    email = models.CharField(max_length=255, verbose_name='email')
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=255, verbose_name='Дом')
    flat = models.CharField(max_length=255, verbose_name='Квартира')
    comment = models.TextField(verbose_name='Комментарий')
    payment_method = models.CharField(max_length=255, verbose_name='Способ оплаты')
    delivery_option = models.CharField(max_length=255, verbose_name='Вариант доставки')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)


class Services(models.Model):
    size = models.CharField(max_length=255, verbose_name='Размер')
    montage = models.CharField(max_length=255, verbose_name='Монтаж')
    elongated_neck = models.CharField(max_length=255, verbose_name='Удлиняющая горловина')
    mounting_neck = models.CharField(max_length=255, verbose_name='Монтаж горловины')
    water_disposal = models.CharField(max_length=255, verbose_name='Водоотведение')
    additional_options = models.CharField(max_length=255, verbose_name='Дополнительные опции')


class Specifications(models.Model):
    dimensions = models.CharField(max_length=255, verbose_name='Габариты')
    station_height = models.CharField(max_length=255, verbose_name='Высота корпуса станции')
    station_weight = models.CharField(max_length=255, verbose_name='Вес станции')
    people_amount = models.IntegerField(verbose_name='Количество пользователей')
    maximum_reset = models.CharField(max_length=255, verbose_name='Максимальный залповый сброс')
    power = models.CharField(max_length=255, verbose_name='Потребляемая мощность')


class PhotoAlbum(models.Model):
    photo = models.ImageField(upload_to=f'photos/', verbose_name='Главное фото')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
