from django.urls import path
from .views import dashboard, mapa, bienvenida

urlpatterns = [
    path('',           bienvenida, name='bienvenida'),
    path('dashboard/', dashboard,  name='dashboard'),
    path('mapa/',      mapa,       name='mapa'),
]