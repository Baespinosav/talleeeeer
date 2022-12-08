from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name="Id de categoría")
    nombreCategoria = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre de la categoría")

    def __str__(self):
        return f"{self.idCategoria} - {self.nombreCategoria}"

class Productos(models.Model):
    patente = models.CharField(max_length=6, primary_key=True, verbose_name="ID")
    marca = models.CharField(max_length=80, blank=False, null=False, verbose_name="Servicio")
    modelo = models.CharField(max_length=80, null=True, blank=True, verbose_name="Tipo de servicio")
    imagen = models.ImageField(upload_to="images/", default="sinfoto.jpg", null=False, blank=False, verbose_name="Imagen")
    precio = models.DecimalField(max_digits=35, decimal_places=2, null=False, blank=False, verbose_name="Precio")
    estado = models.CharField(max_length=80, null=True, blank=True, verbose_name="Estado")
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return f"{self.patente} - {self.marca}, {self.modelo}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name} ({self.user.email})"

class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    orden_compra = models.IntegerField(null=True, blank=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.CharField(max_length=70)
    monto = models.IntegerField(null=True, blank=True)
    estado = models.CharField(null=True ,max_length=70)
    fecha_compra = models.DateField(blank=True, null=True)

    def str(self):
        return f"{self.orden_compra} - {self.correo}"







class Productos2(models.Model):
    patente = models.CharField(max_length=6, primary_key=True, verbose_name="ID")
    marca = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre Comida")
    modelo = models.CharField(max_length=80, null=True, blank=True, verbose_name="Tipo de servicio")
    imagen = models.ImageField(upload_to="images/", default="sinfoto.jpg", null=False, blank=False, verbose_name="Imagen")
    precio = models.DecimalField(max_digits=35, decimal_places=2, null=False, blank=False, verbose_name="Precio")
    estado = models.CharField(max_length=80, null=True, blank=True, verbose_name="Estado")
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)