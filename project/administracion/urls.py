from django.urls import path
from .views import administracion

app_name = 'administracion'

urlpatterns = [
    path('/administracion', administracion, name='administracion'),
]