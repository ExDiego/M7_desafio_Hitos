from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Region(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    
class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    provincia_id = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Tipo_propiedad(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    
class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    
class Propiedad(models.Model):
    nombre = models.CharField(max_length=150, default='', blank=False, null=False)
    descripcion = models.CharField(max_length=200, default='', blank=False, null=False)
    m2_construido = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False, null=False)
    m2_terreno = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False, null=False)
    estacionamientos = models.IntegerField(default=0, blank=False, null=False)
    habitaciones = models.IntegerField(default=0, blank=False, null=False)
    banios = models.IntegerField(default=0, blank=False, null=False)
    direccion = models.CharField(max_length=150, default='', blank=False, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False, null=False)
    uf = models.BooleanField(default=False, blank=False, null=False)
    tipo_propiedad_id = models.ForeignKey(Tipo_propiedad, on_delete=models.CASCADE)
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    
    
