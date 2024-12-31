import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from .models import Usuarios

class UserManagementView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usuarios/user-management.html')

    def post(self, request):
        try:
            data = json.loads(request.body)

            action = data.get('action')

            if action == 'register':
                return self.register_user(data)
            elif action == 'login':
                return self.login_user(request, data)
            else:
                return JsonResponse({'error': 'Acción no válida'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de solicitud inválido'}, status=400)

    def register_user(self, data):
        try:
            username = data.get('username')
            password = data.get('password')
            dni = data.get('dni')
            fecha_nacimiento = data.get('fecha_nacimiento')
            telefono = data.get('telefono')
            domicilio = data.get('domicilio')
            instagram = data.get('instagram')

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'El usuario ya existe'}, status=400)

            user = User.objects.create_user(username=username, password=password)
            Usuarios.objects.create(
                user=user,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                domicilio=domicilio,
                instagram=instagram
            )
            return JsonResponse({'success': 'Usuario registrado correctamente'})
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor al registrar el usuario'}, status=500)

    def login_user(self, request, data):
        try:
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': 'Inicio de sesión exitoso'})
            else:
                return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor al iniciar sesión'}, status=500)