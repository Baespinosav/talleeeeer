from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Productos, Categoria, PerfilUsuario
from .views import administrar_productos

def poblar_bd(request):
    try:
        print("Verificar si existe usuario cliente.")
        if User.objects.filter(username="usuario_cliente").exists():
            print("Intentando eliminar usuario cliente.")
            User.objects.get(username="usuario_cliente").delete()
            print("Usuario cliente eliminado.")
        print("Iniciando creación de usuario cliente.")
        user = User.objects.create_user(username="usuario_cliente", password='Duoc@123')
        user.first_name = "Javiera"
        user.last_name = "Bermudez (Cliente)"
        user.email = "jber@duoc.com"
        user.is_superuser = False
        user.is_staff = False
        PerfilUsuario.objects.create(user=user, rut="11.111.111-K", direccion="Santiago")
        user.save()
        print("Usuario cliente fue creado correctamente.")
    except Exception as err:
        print(f"Error al crear usuario cliente: {err}")
    try:
        print("Verificar si existe usuario staff.")
        if User.objects.filter(username="usuario_staff").exists():
            print("Intentando eliminar usuario staff.")
            User.objects.get(username="usuario_staff").delete()
            print("Usuario staff eliminado.")
        print("Iniciando creación de usuario staff.")
        user = User.objects.create_user(username="usuario_staff", password='Duoc@123')
        user.first_name = "Bastian"
        user.last_name = "Espinosa (Owner)"
        user.email = "baes@duoc.com"
        user.is_superuser = True
        user.is_staff = True
        PerfilUsuario.objects.create(user=user, rut="22.222.222-K", direccion="Santiago")
        user.save()
        print("Usuario staff fue creado correctamente.")
    except Exception as err:
        print(f"Error al crear usuario staff: {err}")
    