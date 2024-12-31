from django.urls import path
from .views import UserManagementView

app_name = 'usuarios'

urlpatterns = [
    path('user-management/', UserManagementView.as_view(), name='user_management'),
]