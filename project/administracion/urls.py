from django.urls import path
from .views import administracion, HorasView, GastosView, PagosView, UsuariosView, Cargar_usuarios

app_name = 'administracion'

urlpatterns = [
    path('', administracion, name='administracion'),
    path('gastos/', GastosView.as_view(), name='gastos'),
    path('horas/', HorasView.as_view(), name='horas'),
    path('pagos/', PagosView.as_view(), name='pagos'),
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    path('cargar_usuario/', Cargar_usuarios.as_view(), name='cargar_usuarios')
]