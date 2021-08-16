from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('product/<int:prod_id>/', product),
]
