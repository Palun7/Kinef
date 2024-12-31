from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    domicilio = models.CharField(max_length=150)
    instagram = models.CharField(max_length=150, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    cargado = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.dni}'

    @property
    def proximo_vencimiento(self):
        ultimo_pago = self.pagos_set.order_by('-fecha').first() # type: ignore
        if ultimo_pago:
            # Asumamos que el pago es mensual
            return ultimo_pago.fecha + timedelta(days=30)
        return None

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
