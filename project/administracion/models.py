from django.db import models
from usuarios.models import Usuarios

class Horas(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    dia = models.DateField()
    horas = models.IntegerField()

    def __str__(self):
        return f'{self.usuario} - {self.horas}'

    class Meta:
        verbose_name = 'Horas'
        verbose_name_plural = 'Horas'

class Gastos(models.Model):

    class FijoVariable(models.TextChoices):
        FIJO = 'fijo', 'Fijo'
        VARIABLE = 'variable', 'Variable'

    class Mes(models.TextChoices):
        ENERO = 'Enero', 'Enero'
        FEBRERO = 'Febrero', 'Febrero'
        MARZO = 'Marzo', 'Marzo'
        ABRIL = 'Abril', 'Abril'
        MAYO = 'Mayo', 'Mayo'
        JUNIO = 'Junio', 'Junio'
        JULIO = 'Julio', 'Julio'
        AGOSTO = 'Agosto', 'Agosto'
        SEPTIEMBRE = 'Septiembre', 'Septiembre'
        OCTUBRE = 'Octubre', 'Octubre'
        NOVIEMBRE = 'Noviembre', 'Noviembre'
        DICIEMBRE = 'Diciembre', 'Diciembre'

    mes = models.CharField(max_length=10, choices=Mes.choices, null=True, blank=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    concepto = models.CharField(max_length=200)
    monto = models.FloatField()
    fijo_variable = models.CharField(max_length=8, choices=FijoVariable.choices, verbose_name='Fijo o Variable')
    fecha_pago = models.DateField()

    def __str__(self):
        return f'{self.concepto}- ${self.monto}, {self.fijo_variable} - {self.fecha_pago}'

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