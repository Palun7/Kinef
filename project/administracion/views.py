from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from usuarios.models import Usuarios
from django.core.serializers.json import DjangoJSONEncoder
from .models import Horas, Gastos, Pagos
import json


def administracion(request):
    return render(request, 'administracion/administracion.html')

class HorasView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/horas.html')

    def obtener_usuarios(self):
        try:
            usuarios = Usuarios.objects.filter(user__is_superuser=True).values('id', 'user__username')
            return JsonResponse(list(usuarios), safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener usuarios'}, status=500)

    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'cargar':
                return self.carga_horas(data)
            elif action == 'obtener_usuarios':
                return self.obtener_usuarios()
            elif action == 'obtener_horas':
                return self.obtener_horas()
            else:
                return JsonResponse({'error': 'Se produjo un error'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato incorrecto'}, status=400)

    def carga_horas(self, data):
        try:
            usuario_id = data.get('usuario')
            dia = data.get('dia')
            horas = data.get('horas')

            usuario = Usuarios.objects.get(id=usuario_id)
            Horas.objects.create(usuario=usuario, dia=dia, horas=horas)

            return JsonResponse({'success': 'Horas cargadas correctamente'})
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def obtener_horas(self):
        try:
            horas = Horas.objects.select_related('usuario').all().values(
                'id', 'usuario__user__username', 'dia', 'horas'
            )
            return JsonResponse(list(horas), safe=False)
        except Exception as e:
            print(f"Error en obtener_horas: {e}")
            return JsonResponse({'error': 'Error al obtener las horas'}, status=500)

class GastosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/gastos.html')

class PagosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/pagos.html')