from django.db import models
from usuarios.models import Usuarios

class Horas(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    dia = models.DateField()
    horas = models.IntegerField()

    def __str__(self):
        return f'{self.usuario} - {self.dia} - {self.horas}'

    class Meta:
        verbose_name = 'Horas'
        verbose_name_plural = 'Horas'

class Gastos(models.Model):

    usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    concepto = models.CharField(max_length=200)
    monto = models.FloatField()
    fecha_gasto = models.DateField()

    def __str__(self):
        return f'{self.concepto}- ${self.monto}, - {self.fecha_gasto}'

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'

class Pagos(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    monto = models.FloatField()
    modo_pago = models.CharField(max_length=50, null=True, blank=True)
    actividad = models.CharField(max_length=50)
    pase = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.usuario}, {self.actividad} {self.pase}, {self.fecha}'

    class Meta:
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'