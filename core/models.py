
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tecnica(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Obra(models.Model):
    titulo = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="obras")
    descripcion = models.CharField(max_length=100)
    historia = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    es_destacado = models.BooleanField(default=False)
    fue_comprado = models.BooleanField(default=False)
    mensaje = models.CharField(max_length=255, blank=True, null=True)
    tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE)
    colaborador =  models.ForeignKey(User,on_delete=models.CASCADE)
    cliente = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cliente', blank=True, null=True)

    def __str__(self):
        return self.titulo

class CarritoCompras(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    obras = models.ManyToManyField(Obra, blank=True, null=True)

class Compra(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    obras = models.ManyToManyField(Obra)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.username} {self.fecha_compra}"
    
    def calcular_total(self):
        total = sum(obra.precio for obra in self.obras.all())
        return total
