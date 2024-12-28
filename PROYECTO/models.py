from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    def precio_formateado(self):
        return f"${self.precio:,}".replace(',', '.')

class CarritoItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"  

class MetaPersonal(models.Model):
    altura = models.PositiveIntegerField(default=0)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    meta = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_responsable = models.CharField(max_length=255, blank=True)# Usuario responsable de la creación de la meta personal

    def save(self, *args, **kwargs):
        if 'usuario' in kwargs:
            self.usuario_responsable = kwargs.pop('usuario').username
        elif not self.usuario_responsable:
            self.usuario_responsable = "Usuario no encontrado"  # Valor por defecto si no se proporciona un usuario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Meta: {self.meta} | Altura: {self.altura} cm | Peso: {self.peso} kg | Responsable: {self.usuario_responsable}"
    
class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    entrenamiento = models.PositiveIntegerField(help_text="Horas de entrenamiento")
    duracion = models.PositiveIntegerField(help_text="Duración en días")
    rutina = models.CharField(max_length=255, help_text="Nombre de la rutina")
    link_descarga = models.URLField(max_length=200, help_text="Link de descarga de Excel")
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_responsable = models.CharField(max_length=255, blank=True)
      # Usuario responsable de la creación del plan

    def save(self, *args, **kwargs):
        if 'usuario' in kwargs:
            self.usuario_responsable = kwargs.pop('usuario').username
        elif not self.usuario_responsable:
            self.usuario_responsable = "Usuario no encontrado"  # Valor por defecto si no se proporciona un usuario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Nombre: {self.nombre} | Entrenador: {self.usuario_responsable}"

class UserPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    fecha_union = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} unido a {self.plan.nombre}"

 