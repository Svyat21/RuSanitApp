from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.IntegerField(verbose_name='Цена')
    people_amount = models.IntegerField(verbose_name='Рекомендуемое количество пользователей')
    short_description = models.CharField(max_length=255, verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание продукта')
    # services =
    in_stock = models.IntegerField(verbose_name='остаток на стоке')
    # customer =
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    main_photo = models.ImageField(upload_to='photos/', verbose_name='Главное фото')
    # photo_album =
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # slug =

    def __str__(self):
        return f'{self.pk}. {self.name}'
