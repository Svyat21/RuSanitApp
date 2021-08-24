from django import forms
from shop.models import *

installation = [
    (True, 'Да'),
    (False, 'Не выбрано'),
]
neck_elongated = [
    ('Не выбрано', 'Не выбрано'),
    ('200мм', '200мм'),
    ('300мм', '300мм'),
    ('400мм', '400мм'),
    ('500мм', '500мм'),
    ('600мм', '600мм'),
    ('700мм', '700мм'),
]
neck_installation = [
    (True, 'Да'),
    (False, 'Не выбрано'),
]
water_dispos = [
    (True, 'Да'),
    (False, 'Не выбрано'),
]
options_additional = [
    ('Не выбрано', 'Не выбрано'),
    ('Аварийная сигнализация', 'Аварийная сигнализация'),
    ('Компрессор HIBLOW', 'Компрессор HIBLOW'),
    ('Компрессор HIBLOW + сигнализация', 'Компрессор HIBLOW + сигнализация'),
]


class ServicesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.sizes = kwargs.pop('sizes')
        super(ServicesForm, self).__init__(*args, **kwargs)
        self.fields['size'] = forms.ChoiceField(choices=self.sizes, label='Размер',
                                                required=False, empty_label='Не выбрано')
    montage = forms.ChoiceField(choices=installation, label='Монтаж', empty_label='Не выбрано')
    elongated_neck = forms.ChoiceField(choices=neck_elongated, label='Удлиняющая горловина', empty_label='Не выбрано')
    mounting_neck = forms.ChoiceField(choices=neck_installation, label='Монтаж горловины', empty_label='Не выбрано')
    water_disposal = forms.ChoiceField(choices=water_dispos, label='Водоотведение', empty_label='Не выбрано')
    additional_options = forms.ChoiceField(choices=options_additional, label='Дополнительные опции',
                                           empty_label='Не выбрано')
