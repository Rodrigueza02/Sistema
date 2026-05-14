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
            self.stdout.write(f'Superusuario "{username}" ya existe. Nada que hacer.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            rol='admin',
            first_name='Admin',
            last_name='SGA',
        )
        self.stdout.write(
            self.style.SUCCESS(f'Superusuario "{username}" creado exitosamente.')
        )
