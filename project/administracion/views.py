from django.shortcuts import render

def administracion(request):
    return render(request, 'administracion/administracion.html')

def horas(request):
    return render(request, 'administracion/horas.html')

def gastos(request):
    return render(request, 'administracion/gastos.html')

def pagos(request):
    return render(request, 'administracion/pagos.html')