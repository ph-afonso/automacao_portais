from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User, Portal, PortalCredential, UserLog
from .serializers import UserSerializer, PortalSerializer, PortalCredentialSerializer

# --- 1. Login Customizado (Já tínhamos) ---
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)

        # Log de Login
        UserLog.objects.create(user=user, action="Efetuou Login no Sistema")

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

# --- 2. Mixin de Auditoria (O Segredo) ---
# Qualquer ViewSet que herdar isso vai gerar logs automaticamente com o usuário correto
class AuditLogMixin:
    def _log_action(self, user, action_verb, instance):
        # Tenta pegar o nome amigável do modelo (Ex: "Portal" ou "Credencial")
        model_name = instance._meta.verbose_name.title()
        action = f"{action_verb} {model_name}: {str(instance)}"
        
        UserLog.objects.create(user=user, action=action)

    def perform_create(self, serializer):
        instance = serializer.save()
        self._log_action(self.request.user, "Criou", instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._log_action(self.request.user, "Editou", instance)

    def perform_destroy(self, instance):
        # Guardamos a string antes de deletar, senão o objeto some
        instance_str = str(instance) 
        model_name = instance._meta.verbose_name.title()
        instance.delete()
        
        action = f"Excluiu {model_name}: {instance_str}"
        UserLog.objects.create(user=self.request.user, action=action)


# --- 3. ViewSets (Agora com Auditoria) ---

class UserViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PortalViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = Portal.objects.all()
    serializer_class = PortalSerializer
    permission_classes = [permissions.IsAuthenticated]

class PortalCredentialViewSet(AuditLogMixin, viewsets.ModelViewSet):
    serializer_class = PortalCredentialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PortalCredential.objects.all()
        return PortalCredential.objects.filter(user=user)
    
    # Ao criar uma credencial, força o dono a ser o usuário logado (segurança)
    def perform_create(self, serializer):
        # Chamamos o save passando o user, e depois chamamos o log manualmente
        # para não conflitar com o AuditLogMixin padrão
        instance = serializer.save(user=self.request.user)
        self._log_action(self.request.user, "Criou", instance)
        