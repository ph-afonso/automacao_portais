from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from core.views import CustomAuthToken, UserViewSet, PortalViewSet, PortalCredentialViewSet

# Configura o Roteador Automático (Agora em PT-BR)
router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'portais', PortalViewSet)
router.register(r'credenciais', PortalCredentialViewSet, basename='credenciais')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', CustomAuthToken.as_view()),
    
    # As rotas ficarão: /api/portais/, /api/usuarios/, etc.
    path('api/', include(router.urls)), 
]

# Configuração para servir as imagens (Logos) durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)