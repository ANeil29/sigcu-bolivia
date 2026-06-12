from rest_framework import serializers
from .models import TipoFase, ProcesoCurricular, FaseProceso

class TipoFaseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TipoFase
        fields = '__all__'

class FaseProcesoSerializer(serializers.ModelSerializer):
    tipo_fase_nombre = serializers.CharField(source='tipo_fase.nombre', read_only=True)
    tipo_fase_codigo = serializers.CharField(source='tipo_fase.codigo', read_only=True)

    class Meta:
        model  = FaseProceso
        fields = '__all__'

class ProcesoCurricularSerializer(serializers.ModelSerializer):
    fases                = FaseProcesoSerializer(many=True, read_only=True)
    tipo_proceso_display = serializers.CharField(source='get_tipo_proceso_display', read_only=True)
    estado_display       = serializers.CharField(source='get_estado_display',       read_only=True)
    anios_desde_conclusion = serializers.ReadOnlyField()

    carrera_nombre      = serializers.CharField(source='carrera.nombre',                     read_only=True)
    universidad_sigla   = serializers.CharField(source='carrera.sede.facultad.universidad.sigla', read_only=True)

    class Meta:
        model  = ProcesoCurricular
        fields = '__all__'