from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from academic.models import Materia, Curso, Nota, Asistencia
from accounts.models import CustomUser


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        total_estudiantes = CustomUser.objects.filter(rol='estudiante', activo=True).count()
        total_docentes    = CustomUser.objects.filter(rol='docente',    activo=True).count()
        total_materias    = Materia.objects.filter(activa=True).count()
        total_cursos      = Curso.objects.count()

        ctx['stats'] = [
            {
                'label': 'Estudiantes',
                'valor': total_estudiantes,
                'icon':  'fas fa-user-graduate',
                'bg':    'bg-purple-100',
                'color': 'text-purple-600',
            },
            {
                'label': 'Docentes',
                'valor': total_docentes,
                'icon':  'fas fa-chalkboard-teacher',
                'bg':    'bg-blue-100',
                'color': 'text-blue-600',
            },
            {
                'label': 'Materias activas',
                'valor': total_materias,
                'icon':  'fas fa-book',
                'bg':    'bg-green-100',
                'color': 'text-green-600',
            },
            {
                'label': 'Cursos',
                'valor': total_cursos,
                'icon':  'fas fa-layer-group',
                'bg':    'bg-yellow-100',
                'color': 'text-yellow-600',
            },
        ]
        return ctx
