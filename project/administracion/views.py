from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from usuarios.models import Usuarios, validate_image
from .models import Horas, Gastos, Pagos
from datetime import datetime
from django.utils.timezone import now
import json
from django.contrib.auth.models import User
from django.forms import ValidationError


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
            fecha = data.get('fecha')

            usuario = Usuarios.objects.get(id=usuario_id)

            Pagos.objects.create(usuario=usuario, monto=monto, modo_pago=modo_pago, actividad=actividad, pase=pase, fecha=fecha)
            return JsonResponse({'success': 'Pago cargado correctamente'})
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
                data.append(pago)
            return JsonResponse(data, safe=False)
        except Exception:
            return JsonResponse({'error': 'Error al obtener los pagos'}, status=500)

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

class Cargar_usuarios(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'administracion/cargar_usuarios.html')

    def post(self, request):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                action = data.get('action')
            else:
                action = request.POST.get('action')

            if action == 'register':
                return self.register_user(request)
            else:
                return JsonResponse({'error': 'Acción no válida'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de solicitud inválido'}, status=400)

    def register_user(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            mail = request.POST.get('mail')
            dni = request.POST.get('dni')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            telefono = request.POST.get('telefono')
            domicilio = request.POST.get('domicilio')
            instagram = request.POST.get('instagram')
            foto = request.FILES.get('foto')

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'El usuario ya existe'}, status=400)

            if Usuarios.objects.filter(dni=dni).exists():
                return JsonResponse({'error': 'El DNI ya está cargado'}, status=400)

            if not dni or len(dni) != 8 or not dni.isdigit():
                return JsonResponse({'error': 'El DNI debe tener 8 dígitos numéricos'}, status=400)

            if foto:
                try:
                    validate_image(foto)
                except ValidationError as e:
                    return JsonResponse({'error': str(e)}, status=400)

            user = User.objects.create_user(username=username, password=password)
            Usuarios.objects.create(
                user=user,
                nombre=nombre,
                apellido=apellido,
                mail=mail,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                domicilio=domicilio,
                instagram=instagram,
                foto=foto
            )
            return JsonResponse({'success': f'{username} se ha registrado con éxito'})
        except Exception:
            return JsonResponse({'error': 'Error al intentar registrar, verifique los datos'}, status=500)