from django.contrib import admin
from shop.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_published', 'date_create', 'date_update')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    list_filter = ('name', 'price', 'is_published', 'date_create', 'date_update')
    prepopulated_fields = {'slug': ('name',)}
    #search_fields = () #по каким полям можно будет осуществлять поиск в админке


class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'photo')
    list_display_links = ('id', 'product')


class SizeProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'price', 'product')
    list_display_links = ('id', 'product')


admin.site.register(Product, ProductAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
admin.site.register(SizeProduct, SizeProductAdmin)
admin.site.register(Montage)
admin.site.register(MountingNeck)
admin.site.register(WaterDisposal)
admin.site.register(ElongatedNeck)
admin.site.register(AdditionalOptions)
admin.site.register(Services)
admin.site.register(Specifications)
admin.site.register(Customer)
admin.site.register(Order)
