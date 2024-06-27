from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from admin_confirm import AdminConfirmMixin

class ObraModelAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['titulo','imagen', 'precio']

# Register your models here.
admin.site.register(Compra)
admin.site.register(Tecnica)
admin.site.register(CarritoCompras)
admin.site.register(Obra, ObraModelAdmin)