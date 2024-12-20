from django.urls import path
from .views import login

app_name = 'usuarios'

urlpatterns = [
    path('/login', login, name='login'),
]