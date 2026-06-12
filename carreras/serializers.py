from rest_framework import serializers
from .models import Carrera, PlanEstudio

class PlanEstudioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PlanEstudio
        fields = '__all__'

class CarreraSerializer(serializers.ModelSerializer):
    planes_estudio  = PlanEstudioSerializer(many=True, read_only=True)
    estado_rediseno = serializers.ReadOnlyField()
    anios_desde_ultimo_rediseno = serializers.ReadOnlyField()

    sede_nombre        = serializers.CharField(source='sede.nombre',                       read_only=True)
    facultad_nombre    = serializers.CharField(source='sede.facultad.nombre',              read_only=True)
    universidad_sigla  = serializers.CharField(source='sede.facultad.universidad.sigla',   read_only=True)
    ciudad             = serializers.CharField(source='sede.ciudad',                       read_only=True)

    class Meta:
        model  = Carrera
        fields = '__all__'