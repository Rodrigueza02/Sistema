from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from academic.models import Nota, Asistencia, Materia, Curso
from accounts.models import CustomUser

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['stats'] = [
            {
                'label': 'Estudiantes',
                'valor': CustomUser.objects.filter(rol='estudiante', activo=True).count(),
                'icon':  'fas fa-user-graduate',
                'bg':    'bg-purple-100',
                'color': 'text-purple-600',
            },
            {
                'label': 'Docentes',
                'valor': CustomUser.objects.filter(rol='docente', activo=True).count(),
                'icon':  'fas fa-chalkboard-teacher',
                'bg':    'bg-blue-100',
                'color': 'text-blue-600',
            },
            {
                'label': 'Materias',
                'valor': Materia.objects.filter(activa=True).count(),
                'icon':  'fas fa-book-open',
                'bg':    'bg-emerald-100',
                'color': 'text-emerald-600',
            },
            {
                'label': 'Cursos Activos',
                'valor': Curso.objects.count(),
                'icon':  'fas fa-school',
                'bg':    'bg-amber-100',
                'color': 'text-amber-600',
            },
        ]
        return ctx