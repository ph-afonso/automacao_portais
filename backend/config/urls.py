from django.contrib import admin
from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token # <--- REMOVA OU COMENTE ESTA LINHA
from core.views import CustomAuthToken # <--- IMPORTE A NOSSA VIEW NOVA

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # path('api/login/', obtain_auth_token), # <--- REMOVA A ANTIGA
    path('api/login/', CustomAuthToken.as_view(), name='api_token_auth'), # <--- USE A NOVA
]