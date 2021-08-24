from django.contrib import admin
from shop.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_published', 'date_create', 'date_update')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    list_filter = ('name', 'price', 'is_published', 'date_create', 'date_update')
    prepopulated_fields = {'slug': ('name',)}
    #search_fields = () #по каким полям можно будет осуществлять поиск в админке


admin.site.register(Product, ProductAdmin)
admin.site.register(SizeProduct)
admin.site.register(Specifications)
admin.site.register(Services)
admin.site.register(PhotoAlbum)
