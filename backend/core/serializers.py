from rest_framework import serializers
from .models import User, Portal, PortalCredential, UserLog

# 1. Serializer de Usuário
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        # Protege a senha para não ser lida, mas permite ser escrita (criada)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Garante que a senha seja criptografada ao criar usuário
        user = User.objects.create_user(**validated_data)
        return user

# 2. Serializer de Portal
class PortalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portal
        fields = '__all__' # Pega todos os campos (nome, link, logo, shared_login...)

# 3. Serializer de Credenciais (Senha do robô)
class PortalCredentialSerializer(serializers.ModelSerializer):
    portal_name = serializers.CharField(source='portal.name', read_only=True)
    
    class Meta:
        model = PortalCredential
        fields = ['id', 'user', 'portal', 'portal_name', 'portal_username', 'portal_password', 'updated_at']

        read_only_fields = ['user']