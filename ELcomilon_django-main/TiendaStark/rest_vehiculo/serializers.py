from rest_framework import serializers
from core.models import Productos

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['patente', 'marca', 'modelo', 'imagen', 'precio', 'categoria']