from django.contrib import admin
from Store.models import Category, Customer, Picture, Shoe, Ad, Size, ShoeSize, AdSize, Order, OrderItem, Ticket
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class PictureAdmin(admin.ModelAdmin):
    pass

class ShoesAdmin(admin.ModelAdmin):
    pass

class AdsAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

class OrderItemAdmin(admin.ModelAdmin):
    pass

class TicketAdmin(admin.ModelAdmin):
    pass

class SizeAdmin(admin.ModelAdmin):
    pass

class ShoesSizeAdmin(admin.ModelAdmin):
    pass

class AdsSizeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shoe, ShoesAdmin)
admin.site.register(Ad, AdsAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ShoeSize, ShoesSizeAdmin)
admin.site.register(AdSize, AdsSizeAdmin)
