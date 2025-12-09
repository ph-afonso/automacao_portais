from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Portal, PortalCredential, UserLog

# 1. Configuração do Usuário
# Usamos o UserAdmin padrão para manter a funcionalidade de alterar senha hashada
admin.site.register(User, UserAdmin)

# 2. Configuração do Portal
@admin.register(Portal)
class PortalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'is_shared_login', 'created_at')
    search_fields = ('name', 'link')
    list_filter = ('is_shared_login',)

# 3. Configuração das Credenciais
@admin.register(PortalCredential)
class PortalCredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'portal', 'portal_username', 'updated_at')
    search_fields = ('user__username', 'portal__name', 'portal_username')
    list_filter = ('portal',)

# 4. Configuração dos Logs (Somente Leitura para segurança)
@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'action_short')
    list_filter = ('created_at', 'user')
    search_fields = ('action', 'user__username')
    readonly_fields = ('user', 'action', 'created_at') # Ninguém deve editar logs

    # Função auxiliar para não mostrar textos gigantes na lista
    def action_short(self, obj):
        return obj.action[:50] + "..." if len(obj.action) > 50 else obj.action
    action_short.short_description = "Ação"

    # Impede de adicionar logs manualmente pelo admin
    def has_add_permission(self, request):
        return False