from django.urls import path
from .views import *

urlpatterns = [
    path('crearnotas/', CrearNotas, name='Crear Notas'),
    path('editarnota/<int:idnota>', EditarNota, name='Editar Notas'),
    path('eliminarnota/<int:idnota>', EliminarNota, name='Eliminar Notas'),
    path('notas/', MisNotas, name='Mis Notas'),
    path('registrarse/', Registrarse, name='Registrarse'),
    path('', IniciarSesion, name='Iniciar Sesion'),
    path('cerrarsesion/', CerrarSesion, name='Cerrar Sesion'),
]
