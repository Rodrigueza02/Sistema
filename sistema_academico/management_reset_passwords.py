"""
Script para establecer contraseñas conocidas
Ejecutar: python management_reset_passwords.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

# Definir contraseñas simples para pruebas
usuarios_passwords = {
    'helenadmin': 'admin123',
    'helendocente': 'docente123',
    'helenestudiante': 'estudiante123',
}

print("=" * 50)
print("ESTABLECIENDO CONTRASEÑAS DE PRUEBA")
print("=" * 50)

for username, password in usuarios_passwords.items():
    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✓ Usuario: {username}")
        print(f"  Contraseña: {password}")
        print(f"  Rol: {user.get_rol_display()}")
        print(f"  Email: {user.email}")
        print("-" * 50)
    except CustomUser.DoesNotExist:
        print(f"✗ Usuario '{username}' no encontrado")
        print("-" * 50)

print("\n¡Contraseñas actualizadas exitosamente!")
print("\nCREDENCIALES PARA EL MANUAL:")
print("=" * 50)
for username, password in usuarios_passwords.items():
    try:
        user = CustomUser.objects.get(username=username)
        print(f"- **Usuario {user.get_rol_display()}:**")
        print(f"  - Username: `{username}`")
        print(f"  - Password: `{password}`")
    except CustomUser.DoesNotExist:
        pass
print("=" * 50)
