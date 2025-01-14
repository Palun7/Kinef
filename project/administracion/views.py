from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from usuarios.models import Usuarios
from .models import Horas, Gastos, Pagos
from datetime import datetime
from django.utils.timezone import now
import json


def administracion(request):
    return render(request, 'administracion/administracion.html')

class HorasView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/horas.html')

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
            elif action == 'sumar_horas':
                return self.horas_este_mes()
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
        except Exception:
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def obtener_usuarios(self):
        try:
            usuarios = Usuarios.objects.filter(user__is_superuser=True).values('id', 'user__username')
            return JsonResponse(list(usuarios), safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener usuarios'}, status=500)

    def obtener_horas(self):
        try:
            horas = Horas.objects.select_related('usuario').all().values(
                'id', 'usuario__user__username', 'dia', 'horas'
            )
            data = []
            for hora in horas:
                hora['dia'] = hora['dia'].strftime('%Y/%m/%d') 
                data.append(hora)
            return JsonResponse(data, safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener las horas'}, status=500)

    def horas_este_mes(self):
        try:
            # Obtener el mes y año actuales
            fecha_actual = now()
            mes_actual = fecha_actual.month
            año_actual = fecha_actual.year

            # Filtrar las horas del mes y año actuales
            horas = Horas.objects.filter(dia__year=año_actual, dia__month=mes_actual).select_related('usuario').values(
                'id', 'usuario__user__username', 'dia', 'horas'
            )

            data = []
            for hora in horas:
                hora['dia'] = hora['dia'].strftime('%Y-%m-%d')  # Formatear la fecha para JSON
                data.append(hora)

            return JsonResponse(data, safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener las horas del mes'}, status=500)

class GastosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/gastos.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'cargar':
                return self.carga_gastos(data)
            elif action == 'obtener_usuarios':
                return self.obtener_usuarios()
            elif action == 'obtener_gastos':
                return self.obtener_gastos()
            else:
                return JsonResponse({'error': 'Se produjo un error'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato incorrecto'}, status=400)

    def carga_gastos(self, data):
        try:
            usuario_id = data.get('usuario')
            concepto = data.get('concepto')
            monto = float(data.get('monto', 0))
            fecha_gasto = datetime.strptime(data.get('fecha_gasto'), '%Y-%m-%d').date()

            usuario = Usuarios.objects.get(id=usuario_id)
            if not concepto or len(concepto) > 200:
                return JsonResponse({'error': 'El concepto es inválido'}, status=400)
            if not isinstance(monto, (float, int)) or monto <= 0:
                return JsonResponse({'error': 'El monto es inválido'}, status=400)

            Gastos.objects.create(usuario=usuario, concepto=concepto, monto=monto, fecha_gasto=fecha_gasto)
            return JsonResponse({'success': 'Gasto cargado correctamente'})
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception:
            return JsonResponse({'error': 'Error al cargar'}, status=400)

    def obtener_usuarios(self):
        try:
            usuarios = Usuarios.objects.filter(user__is_superuser=True).values('id', 'user__username')
            return JsonResponse(list(usuarios), safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener usuarios'}, status=500)

    def obtener_gastos(self):
        try:
            gastos = Gastos.objects.select_related('usuario').all().values(
                'usuario__user__username', 'concepto', 'monto', 'fecha_gasto'
            )
            data = []
            for gasto in gastos:
                gasto['fecha_gasto'] = gasto['fecha_gasto'].strftime('%d/%m/%Y') 
                print(gasto)
                data.append(gasto)
            return JsonResponse(data, safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener las horas'}, status=500)

class PagosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/pagos.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'cargar':
                return self.carga_pagos(data)
            elif action == 'obtener_usuarios':
                return self.obtener_usuarios()
            elif action == 'obtener_pagos':
                return self.obtener_pagos()
            else:
                return JsonResponse({'error': 'Se produjo un error'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato incorrecto'}, status=400)

    def carga_pagos(self, data):
        try:
            usuario_id = data.get('usuario')
            monto = data.get('monto')
            modo_pago = data.get('modo_pago')
            actividad = data.get('actividad')
            pase = data.get('pase')

            usuario = Usuarios.objects.get(id=usuario_id)

            Pagos.objects.create(usuario=usuario, monto=monto, modo_pago=modo_pago, actividad=actividad, pase=pase)
            return JsonResponse({'success': 'Gasto cargado correctamente'})
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception:
            return JsonResponse({'error': 'Error al cargar'}, status=400)

    def obtener_usuarios(self):
        try:
            usuarios = Usuarios.objects.filter().values('id', 'user__username', 'dni')
            return JsonResponse(list(usuarios), safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener usuarios'}, status=500)

    def obtener_pagos(self):
        try:
            pagos = Pagos.objects.select_related('usuario').all().values(
                'usuario__user__username', 'monto', 'modo_pago', 'actividad', 'pase', 'fecha'
            )

            data = []
            for pago in pagos:
                pago['fecha'] = pago['fecha'].strftime('%d/%m/%Y') 
                print(pago)
                data.append(pago)
            return JsonResponse(data, safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener las horas'}, status=500)

class UsuariosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/usuarios.html')

    def post(self,request):
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'obtener_usuarios':
                return self.obtener_usuarios()
            else:
                return JsonResponse({'error': 'Se produjo un error'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato incorrecto'}, status=400)

    def obtener_usuarios(self):
        try:
            usuarios = Usuarios.objects.all()
            usuarios_data = [
                {
                    'user__username': usuario.user.username,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'mail': usuario.mail if usuario.mail else '-',
                    'dni': usuario.dni,
                    'telefono': usuario.telefono,
                    'domicilio': usuario.domicilio,
                    'fecha_nacimiento': usuario.fecha_nacimiento.strftime('%d/%m/%Y') if usuario.fecha_nacimiento else None,
                    'instagram': usuario.instagram if usuario.instagram else '-',
                    'foto': usuario.foto.url if usuario.foto else None,
                    'cargado': usuario.cargado.strftime('%d/%m/%Y') if usuario.cargado else None,
                }
                for usuario in usuarios
            ]
            return JsonResponse(usuarios_data, safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener usuarios'}, status=500)