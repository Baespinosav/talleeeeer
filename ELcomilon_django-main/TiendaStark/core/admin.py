from django.contrib import admin
from .models import Categoria, Productos, PerfilUsuario, Ventas

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Productos)
admin.site.register(PerfilUsuario)
admin.site.register(Ventas)

