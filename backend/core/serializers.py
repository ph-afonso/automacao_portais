from rest_framework import serializers
from .models import User, Portal, PortalCredential, UserLog

# 1. Serializer de Usuário
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff']
        # Isso garante que a senha só pode ser escrita, nunca lida (segurança)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Remove a senha dos dados validados para tratar separadamente
        password = validated_data.pop('password', None)
        
        # Cria a instância do usuário com o restante dos dados
        instance = self.Meta.model(**validated_data)
        
        # Se a senha foi enviada, usa o método set_password para criptografar
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Mesma lógica para o Update
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

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