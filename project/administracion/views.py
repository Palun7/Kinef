from django.shortcuts import render

def administracion(request):
    return render(request, 'administracion/administracion.html')
