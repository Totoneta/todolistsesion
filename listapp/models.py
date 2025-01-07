from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, blank=False)
    apellido = models.CharField(max_length=30, blank=False)
    dni = models.IntegerField(unique=True, blank=False)
    fechadenacimiento = models.DateField(blank=False)
    email = models.EmailField(unique=True, blank=False)
    fechaderegistro = models.DateTimeField(auto_now_add=True)

class Nota(models.Model):
    titulo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    finalizada = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.titulo} {self.descripcion} {self.finalizada}'