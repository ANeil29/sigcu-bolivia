from django.urls import path
from .views import dashboard, mapa

urlpatterns = [
    path('',      dashboard, name='dashboard'),
    path('mapa/', mapa,      name='mapa'),
]