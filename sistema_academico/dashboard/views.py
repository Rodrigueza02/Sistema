from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from academic.models import Materia, Curso, Nota, Asistencia
from accounts.models import CustomUser


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        if user.es_estudiante():
            return self._ctx_estudiante(ctx, user)
        elif user.es_docente():
            return self._ctx_docente(ctx, user)
        else:
            return self._ctx_admin(ctx)

    # ── Admin ─────────────────────────────────────────────────────────────
    def _ctx_admin(self, ctx):
        ctx['rol_dashboard'] = 'admin'
        ctx['stats'] = [
            {
                'label': 'Estudiantes activos',
                'valor': CustomUser.objects.filter(rol='estudiante', activo=True).count(),
                'icon':  'fas fa-user-graduate',
                'bg':    'bg-purple-100',
                'color': 'text-purple-600',
            },
            {
                'label': 'Docentes activos',
                'valor': CustomUser.objects.filter(rol='docente', activo=True).count(),
                'icon':  'fas fa-chalkboard-teacher',
                'bg':    'bg-blue-100',
                'color': 'text-blue-600',
            },
            {
                'label': 'Materias activas',
                'valor': Materia.objects.filter(activa=True).count(),
                'icon':  'fas fa-book',
                'bg':    'bg-green-100',
                'color': 'text-green-600',
            },
            {
                'label': 'Cursos',
                'valor': Curso.objects.count(),
                'icon':  'fas fa-layer-group',
                'bg':    'bg-yellow-100',
                'color': 'text-yellow-600',
            },
        ]
        return ctx

    # ── Docente ───────────────────────────────────────────────────────────
    def _ctx_docente(self, ctx, user):
        ctx['rol_dashboard'] = 'docente'

        # Materias que dicta este docente
        mis_materias = Materia.objects.filter(docente=user, activa=True)

        # Notas registradas en sus materias
        notas_mis_materias = Nota.objects.filter(materia__in=mis_materias)

        # Estudiantes únicos en sus materias
        estudiantes_ids = notas_mis_materias.values_list(
            'estudiante', flat=True
        ).distinct()

        # Asistencia en sus materias
        asistencias = Asistencia.objects.filter(materia__in=mis_materias)
        total_asist = asistencias.count()
        presentes   = asistencias.filter(presente=True).count()
        pct_asist   = round((presentes / total_asist * 100), 1) if total_asist > 0 else 0

        ctx['stats'] = [
            {
                'label': 'Mis materias',
                'valor': mis_materias.count(),
                'icon':  'fas fa-book',
                'bg':    'bg-purple-100',
                'color': 'text-purple-600',
            },
            {
                'label': 'Estudiantes',
                'valor': estudiantes_ids.count(),
                'icon':  'fas fa-user-graduate',
                'bg':    'bg-blue-100',
                'color': 'text-blue-600',
            },
            {
                'label': 'Notas registradas',
                'valor': notas_mis_materias.count(),
                'icon':  'fas fa-clipboard-list',
                'bg':    'bg-green-100',
                'color': 'text-green-600',
            },
            {
                'label': '% Asistencia',
                'valor': f'{pct_asist}%',
                'icon':  'fas fa-calendar-check',
                'bg':    'bg-yellow-100',
                'color': 'text-yellow-600',
            },
        ]

        # Promedios por materia del docente
        ctx['promedios_docente'] = list(
            notas_mis_materias
            .values('materia__nombre')
            .annotate(promedio=Avg('valor'))
            .order_by('materia__nombre')
        )

        # Últimas 5 notas registradas por este docente en sus materias
        ctx['ultimas_notas'] = notas_mis_materias.select_related(
            'estudiante', 'materia', 'curso'
        ).order_by('-fecha')[:5]

        ctx['mis_materias'] = mis_materias
        return ctx

    # ── Estudiante ────────────────────────────────────────────────────────
    def _ctx_estudiante(self, ctx, user):
        ctx['rol_dashboard'] = 'estudiante'

        notas       = Nota.objects.filter(estudiante=user)
        asistencias = Asistencia.objects.filter(estudiante=user)
        cursos      = Curso.objects.filter(estudiantes=user)

        promedio_general = notas.aggregate(p=Avg('valor'))['p']
        total_asist      = asistencias.count()
        presentes        = asistencias.filter(presente=True).count()
        pct_asistencia   = round((presentes / total_asist * 100), 1) if total_asist > 0 else 0

        ctx['stats'] = [
            {
                'label': 'Promedio general',
                'valor': f'{promedio_general:.2f}' if promedio_general else '—',
                'icon':  'fas fa-star',
                'bg':    'bg-purple-100',
                'color': 'text-purple-600',
            },
            {
                'label': 'Asistencia',
                'valor': f'{pct_asistencia}%',
                'icon':  'fas fa-calendar-check',
                'bg':    'bg-green-100',
                'color': 'text-green-600',
            },
            {
                'label': 'Cursos inscritos',
                'valor': cursos.count(),
                'icon':  'fas fa-layer-group',
                'bg':    'bg-blue-100',
                'color': 'text-blue-600',
            },
            {
                'label': 'Notas registradas',
                'valor': notas.count(),
                'icon':  'fas fa-clipboard-list',
                'bg':    'bg-yellow-100',
                'color': 'text-yellow-600',
            },
        ]

        ctx['promedios_estudiante'] = list(
            notas.values('materia__nombre')
            .annotate(promedio=Avg('valor'))
            .order_by('materia__nombre')
        )
        ctx['ultimas_notas'] = notas.select_related(
            'materia', 'curso'
        ).order_by('-fecha')[:5]
        ctx['mis_cursos'] = cursos.prefetch_related('materias')[:6]
        return ctx
