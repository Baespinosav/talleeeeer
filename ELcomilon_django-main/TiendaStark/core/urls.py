from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import home, administrar_productos, reportes, tienda, ficha, registro
from .views import iniciar_sesion, registrar_usuario, cerrar_sesion
from .views import perfil_usuario, iniciar_pago, pago_exitoso,reportes_usuarios
from .views import  index
from .views_poblar_bd import poblar_bd

urlpatterns = [
    path('', home, name="home"),
    path('index', index, name="index"),
    path('poblar_bd', poblar_bd, name="poblar_bd"),
    
    path('administrar_productos/<action>/<id>', administrar_productos, name="administrar_productos"),
    
    path('tienda', tienda, name="tienda"),
    path('ficha/<id>', ficha, name="ficha"),
    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    path('password_cambiada/', TemplateView.as_view(template_name='core/password_cambiada.html'), name='password_cambiada'),
    path('cambiar_password/', auth_views.PasswordChangeView.as_view(template_name='core/cambiar_password.html', success_url='/password_cambiada'), name='cambiar_password'),
    path('perfil_usuario/', perfil_usuario, name="perfil_usuario"),
    path('iniciar_pago/<id>', iniciar_pago, name="iniciar_pago"),
    path('pago_exitoso/', pago_exitoso, name="pago_exitoso"),
    path('registro/', registro, name="registro"),
    path('reportes/', reportes, name="reportes"),
    path('reportes_usuarios/', reportes_usuarios, name="reportes_usuarios"),
]