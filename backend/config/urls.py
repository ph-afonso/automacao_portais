from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # <--- Importante

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Essa view mágica recebe username/password e devolve o Token
    path('api/login/', obtain_auth_token, name='api_token_auth'), 
]