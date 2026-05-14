from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN    = 'admin',    'Administrador'
        DOCENTE  = 'docente',  'Docente'
        ESTUDIANTE = 'estudiante', 'Estudiante'

    rol     = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)
    activo  = models.BooleanField(default=True)
    #foto    = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)

    def es_admin(self):     return self.rol == self.Rol.ADMIN
    def es_docente(self):   return self.rol == self.Rol.DOCENTE
    def es_estudiante(self): return self.rol == self.Rol.ESTUDIANTE

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"