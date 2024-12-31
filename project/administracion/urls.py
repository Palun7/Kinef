from django.urls import path
from .views import administracion, gastos, horas, pagos

app_name = 'administracion'

urlpatterns = [
    path('', administracion, name='administracion'),
    path('gastos/', gastos, name='gastos'),
    path('horas/', horas, name='horas'),
    path('pagos/', pagos, name='pagos'),
]