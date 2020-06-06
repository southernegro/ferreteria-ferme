from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Cliente)
admin.site.register(Seller)
admin.site.register(Supplier)
admin.site.register(Employee)
admin.site.register(Administrator)
admin.site.register(Producto)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(ShippingAddress)
admin.site.register(Boleta)
