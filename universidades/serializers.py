from rest_framework import serializers
from .models import Universidad, Facultad, Sede

class SedeSerializer(serializers.ModelSerializer):
    latitud  = serializers.SerializerMethodField()
    longitud = serializers.SerializerMethodField()

    class Meta:
        model = Sede
        fields = '__all__'

    def get_latitud(self, obj):
        return obj.ubicacion.y if obj.ubicacion else None

    def get_longitud(self, obj):
        return obj.ubicacion.x if obj.ubicacion else None

class FacultadSerializer(serializers.ModelSerializer):
    sedes = SedeSerializer(many=True, read_only=True)

    class Meta:
        model = Facultad
        fields = '__all__'

class UniversidadSerializer(serializers.ModelSerializer):
    facultades = FacultadSerializer(many=True, read_only=True)

    class Meta:
        model = Universidad
        fields = '__all__'