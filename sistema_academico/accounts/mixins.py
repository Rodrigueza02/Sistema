from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class RolRequeridoMixin(LoginRequiredMixin):
    roles_permitidos = []  # Ej: ['admin', 'docente']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.roles_permitidos and request.user.rol not in self.roles_permitidos:
            raise PermissionDenied("No tienes permiso para acceder aquí.")
        return super().dispatch(request, *args, **kwargs)

class SoloAdminMixin(RolRequeridoMixin):
    roles_permitidos = ['admin']

class DocenteOAdminMixin(RolRequeridoMixin):
    roles_permitidos = ['admin', 'docente']