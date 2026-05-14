import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea el superusuario inicial si no existe (para despliegue en Render)'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@sga.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin2026*')

        if User.objects.filter(username=username).exists():
            # Asegurarse de que esté activo y con rol admin aunque ya exista
            user = User.objects.get(username=username)
            updated = False
            if not user.activo:
                user.activo = True
                updated = True
            if user.rol != 'admin':
                user.rol = 'admin'
                updated = True
            if updated:
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Superusuario "{username}" actualizado (activo=True, rol=admin).'
                ))
            else:
                self.stdout.write(f'Superusuario "{username}" ya existe y está correcto.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            rol='admin',
            activo=True,
            first_name='Admin',
            last_name='SGA',
        )
        self.stdout.write(self.style.SUCCESS(
            f'Superusuario "{username}" creado. Usuario: {username} / Pass: {password}'
        ))
