from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from admin_confirm import AdminConfirmMixin

class ObraModelAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['titulo','imagen', 'precio']
class TecnicaModelAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['descripcion']
class CompraModelAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['cliente']
class CarritoModelAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['cliente']

# Register your models here.
admin.site.register(Compra, CompraModelAdmin)
admin.site.register(Tecnica, TecnicaModelAdmin)
admin.site.register(CarritoCompras, CarritoModelAdmin)
admin.site.register(Obra, ObraModelAdmin)