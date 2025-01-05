from django.urls import path
from .views import UserManagementView
from django.contrib.auth.views import LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('user-management/', UserManagementView.as_view(), name='user_management'),
    path('logout/', LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
]