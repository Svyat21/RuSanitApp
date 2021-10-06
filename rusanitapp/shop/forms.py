from django import forms
from shop.models import *

q_montage = Montage.objects.all()
q_elongated_neck = ElongatedNeck.objects.all()
q_mounting_neck = MountingNeck.objects.all()
q_water_disposal = WaterDisposal.objects.all()
q_additional_options = AdditionalOptions.objects.all()


class ServicesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.sizes = kwargs.pop('sizes')
        super(ServicesForm, self).__init__(*args, **kwargs)
        self.fields['size'] = forms.ModelChoiceField(queryset=self.sizes, empty_label='Не выбрано', label='Размер')
    montage = forms.ModelChoiceField(queryset=q_montage, empty_label='Не выбрано', label='Монтаж')
    elongated_neck = forms.ModelChoiceField(queryset=q_elongated_neck, empty_label='Не выбрано',
                                            label='Удлиняющая горловина')
    mounting_neck = forms.ModelChoiceField(queryset=q_mounting_neck, empty_label='Не выбрано', label='Монтаж горловины')
    water_disposal = forms.ModelChoiceField(queryset=q_water_disposal, empty_label='Не выбрано', label='Водоотведение')
    additional_options = forms.ModelChoiceField(queryset=q_additional_options, empty_label='Не выбрано',
                                                label='Дополнительные опции')
    count = forms.IntegerField(label='Количество')


class MakingOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['recipient', 'phone_number', 'email', 'city', 'street', 'house_number',
                  'flat', 'comment', 'payment_method', 'delivery_option']
        widgets = {
            'recipient': forms.TextInput(attrs={'placeholder': 'Получатель'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Телефон'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
            'street': forms.TextInput(attrs={'placeholder': 'Улица'}),
            'house_number': forms.TextInput(attrs={'placeholder': 'Дом'}),
            'flat': forms.TextInput(attrs={'placeholder': 'Квартира'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Комментарий', 'rows': 3}),
            'payment_method': forms.RadioSelect(attrs={'type': 'radio'}),
            'delivery_option': forms.RadioSelect(attrs={'type': 'radio'}),
        }


class FeedbackForm(forms.Form):
    name_attrs = {'placeholder': 'Ваше имя', 'class': 'input-call'}
    phone_attrs = {'placeholder': 'Телефон', 'class': 'input-call'}
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs=name_attrs))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs=phone_attrs))
    checked = forms.BooleanField()


class QuestionForm(forms.Form):
    name_attrs = {'placeholder': 'Ваше имя', 'class': 'input-contacts'}
    phone_attrs = {'placeholder': 'Как с вами связаться', 'class': 'input-contacts'}
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs=name_attrs))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs=phone_attrs))
    question = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение или вопрос'}),
        required=False
    )
