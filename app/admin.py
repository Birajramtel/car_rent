from django.contrib import admin
from .models import Item, OrderItem, Category, Order, Slider, Contact, Trip, BillingAddress, ShippingAddress, Payment
# Register your models here.
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Slider)
admin.site.register(Contact)
admin.site.register(Trip)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
admin.site.register(Payment)
