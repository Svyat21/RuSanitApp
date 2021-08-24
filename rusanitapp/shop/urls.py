from django.urls import path
from .views import *

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('product/<slug:prod_slug>/', show_product, name='product'),
]
