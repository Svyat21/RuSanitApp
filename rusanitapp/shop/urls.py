from django.urls import path
from .views import *

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('product/<slug:prod_slug>/', ShowProduct.as_view(), name='show_product'),
    path('basket/', Basket.as_view(), name='basket')
]
