from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('register/', views.register_view, name='register'),
    
    # CRUD Usuarios (Solo Admin)
    path('usuarios/',                views.UserListView.as_view(),   name='user-list'),
    path('usuarios/crear/',          views.UserCreateView.as_view(), name='user-create'),
    path('usuarios/<int:pk>/editar/', views.UserUpdateView.as_view(), name='user-update'),
    path('usuarios/<int:pk>/toggle/', views.toggle_user_status,       name='user-toggle'),
]
