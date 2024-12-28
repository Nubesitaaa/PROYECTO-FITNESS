from django.contrib import admin
from .models import Producto, MetaPersonal, CarritoItem, Plan

# Register your models here.

admin.site.register(Producto)
admin.site.register(MetaPersonal)
admin.site.register(CarritoItem)
admin.site.register(Plan)
