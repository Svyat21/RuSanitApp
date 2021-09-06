from django.urls import path
from .views import *

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('feedback/', ordering_feedback, name='feedback'),
    path('product/<slug:prod_slug>/', ShowProduct.as_view(), name='show_product'),
    path('basket/', Basket.as_view(), name='basket'),
    path('basket_remove/<int:service_pk>', remove_obj_basket, name='basket_remove'),
    path('order/', MakingOrder.as_view(), name='order')
]
