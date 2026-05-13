from django.core.mail import send_mail
from django.conf import settings

def notificar_nota_email(nota):
    """Envía email al estudiante cuando se registra una nota."""
    estudiante = nota.estudiante
    if not estudiante.email:
        return
    send_mail(
        subject=f'Nueva calificación en {nota.materia.nombre}',
        message=(
            f'Hola {estudiante.first_name},\n\n'
            f'Se ha registrado una nueva nota:\n'
            f'  Materia: {nota.materia.nombre}\n'
            f'  Tipo:    {nota.get_tipo_display()}\n'
            f'  Nota:    {nota.valor}\n\n'
            f'Ingresa al sistema para más detalles.'
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[estudiante.email],
        fail_silently=True,
    )