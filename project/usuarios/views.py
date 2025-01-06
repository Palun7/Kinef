import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from .models import Usuarios, validate_image
from django.forms import ValidationError

class UserManagementView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usuarios/user-management.html')

    def post(self, request):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                action = data.get('action')
            else:
                action = request.POST.get('action')

            if action == 'register':
                return self.register_user(request)
            elif action == 'login':
                return self.login_user(request, data)
            else:
                return JsonResponse({'error': 'Acción no válida'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de solicitud inválido'}, status=400)

    def register_user(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
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

    def login_user(self, request, data):
        try:
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Usuario y contraseña son requeridos'}, status=400)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': f'{username} ha iniciado sesión'})
            else:
                return JsonResponse({'error': 'Usuario o contraseña incorrectos'}, status=401)
        except Exception:
            return JsonResponse({'error': 'Error interno del servidor al iniciar sesión'}, status=500)