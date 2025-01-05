from django.shortcuts import render
from django.views import View
from .models import Horas, Gastos, Pagos


def administracion(request):
    return render(request, 'administracion/administracion.html')

class HorasView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/horas.html')

class GastosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/gastos.html')

class PagosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/pagos.html')