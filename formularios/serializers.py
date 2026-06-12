from rest_framework import serializers
from .models import FormularioValoracion

class FormularioValoracionSerializer(serializers.ModelSerializer):
    estado_display  = serializers.CharField(source='get_estado_display', read_only=True)
    carrera_nombre  = serializers.CharField(source='proceso.carrera.nombre', read_only=True)

    class Meta:
        model  = FormularioValoracion
        fields = '__all__'