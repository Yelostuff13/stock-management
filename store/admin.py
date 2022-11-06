from django.contrib import admin
from store.models import Product,Film,Cart,CartItem,Order,OrderItem
# Register your models here.
class FilmAdmin(admin.ModelAdmin):
    list_display=['name','price','stock','created','updated']
    list_editable=['price','stock']
    list_per_page=15

admin.site.register(Product)
admin.site.register(Film,FilmAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)