from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def notificar_nota_email(nota):
    """Envía email al estudiante cuando se registra una nota."""
    try:
        estudiante = nota.estudiante
        
        # Validar que el estudiante tenga email
        if not estudiante or not estudiante.email:
            logger.warning(f'Estudiante sin email: {estudiante}')
            return
        
        # Validar que EMAIL_HOST_USER esté configurado
        if not settings.EMAIL_HOST_USER:
            logger.warning('EMAIL_HOST_USER no configurado, saltando envío de email')
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
        logger.info(f'Email enviado a {estudiante.email} para nota {nota.id}')
    except Exception as e:
        # Capturar cualquier error y solo loguearlo, no romper la aplicación
        logger.error(f'Error al enviar email de notificación: {str(e)}')
        # No re-lanzar la excepción para que no rompa el guardado de la nota
