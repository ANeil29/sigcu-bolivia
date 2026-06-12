from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)

urlpatterns = [
    path('admin/',                  admin.site.urls),
    path('auth/',                   include('accounts.urls')),        
    path('api/v1/auth/',            include('accounts.urls')),        
    path('api/v1/universidades/',   include('universidades.urls')),
    path('api/v1/carreras/',        include('carreras.urls')),
    path('api/v1/programas/',       include('programas.urls')),
    path('api/v1/seguimiento/',     include('seguimiento.urls')),
    path('api/v1/formularios/',     include('formularios.urls')),
    path('api/v1/reportes/',        include('reportes.urls')),
    path('',                        include('core.urls')),

    path('api/schema/',         SpectacularAPIView.as_view(),                       name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',   SpectacularRedocView.as_view(url_name='schema'),   name='redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)