from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. Classe Base para Datas (Reutilizável)
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        abstract = True

# 2. Usuário Customizado
class User(AbstractUser):
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username

# 3. Portais
class Portal(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Portal")
    link = models.URLField(verbose_name="Link do Portal")
    logo = models.ImageField(upload_to='portais/logos/', null=True, blank=True, verbose_name="Logotipo")
    
    is_shared_login = models.BooleanField(
        default=False, 
        verbose_name="Login Único (Compartilhado)?",
        help_text="Se marcado, o sistema usará as credenciais abaixo para todos os usuários."
    )
    
    # Credenciais Globais
    shared_username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Usuário Global")
    shared_password = models.CharField(max_length=255, blank=True, null=True, verbose_name="Senha Global")

    class Meta:
        verbose_name = "Portal"
        verbose_name_plural = "Portais"
        ordering = ['name']

    def __str__(self):
        return self.name

# 4. Credenciais por Usuário
class PortalCredential(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='credentials',
        verbose_name="Usuário do Sistema"
    )
    portal = models.ForeignKey(
        Portal, 
        on_delete=models.CASCADE, 
        related_name='user_credentials',
        verbose_name="Portal"
    )
    
    portal_username = models.CharField(max_length=150, verbose_name="Login no Portal")
    portal_password = models.CharField(max_length=255, verbose_name="Senha no Portal")

    class Meta:
        verbose_name = "Credencial de Acesso"
        verbose_name_plural = "Credenciais de Acesso"
        unique_together = ('user', 'portal') # Um usuário só pode ter uma senha por portal

    def __str__(self):
        return f"{self.user.username} - {self.portal.name}"

# 5. Logs de Auditoria
class UserLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Usuário"
    )
    action = models.TextField(verbose_name="Ação Realizada")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do Evento")

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at.strftime('%d/%m/%Y %H:%M')}] {self.user} - {self.action}"