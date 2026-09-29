from django.urls import path
from .views import dashboard, mapa, bienvenida, bienvenida_publica

urlpatterns = [
    path('',            bienvenida_publica, name='bienvenida-publica'),
    path('inicio/',     bienvenida,         name='bienvenida'),
    path('dashboard/',  dashboard,          name='dashboard'),
    path('mapa/',       mapa,               name='mapa'),
]