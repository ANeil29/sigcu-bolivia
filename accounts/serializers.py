from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'rol', 'universidad', 'is_active']
        read_only_fields = ['id']

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'rol', 'universidad']

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)