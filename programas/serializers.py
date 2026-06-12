from rest_framework import serializers
from .models import Programa


class ProgramaSerializer(serializers.ModelSerializer):
    estado_display        = serializers.CharField(source='get_estado_display',         read_only=True)
    grado_previsto_display = serializers.CharField(source='get_grado_previsto_display', read_only=True)
    universidad_sigla     = serializers.CharField(source='sede.facultad.universidad.sigla', read_only=True)
    universidad_nombre    = serializers.CharField(source='sede.facultad.universidad.nombre', read_only=True)
    facultad_nombre       = serializers.CharField(source='sede.facultad.nombre',        read_only=True)
    sede_nombre           = serializers.CharField(source='sede.nombre',                 read_only=True)
    ciudad                = serializers.CharField(source='sede.ciudad',                 read_only=True)
    departamento          = serializers.ReadOnlyField()
    dias_desde_inicio     = serializers.ReadOnlyField()
    proximo_a_vencer      = serializers.ReadOnlyField()

    class Meta:
        model  = Programa
        fields = '__all__'