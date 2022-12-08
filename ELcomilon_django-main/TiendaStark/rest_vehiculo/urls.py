from django.urls import path
from django.contrib import admin
from .views import vehiculo_create, vehiculo_read, vehiculo_read_all
from .views import vehiculo_update, vehiculo_delete, login

urlpatterns = [
    path('vehiculo_create/', vehiculo_create.as_view(), name="vehiculo_create"),
    path('vehiculo_update/', vehiculo_update.as_view(), name="vehiculo_update"),
    path('vehiculo_read/<id>/', vehiculo_read, name="vehiculo_read"),
    path('vehiculo_read_all/', vehiculo_read_all, name='vehiculo_read_all'),
    path('vehiculo_delete/<id>/', vehiculo_delete, name="vehiculo_delete"),
    path('login', login, name='login'),
]
