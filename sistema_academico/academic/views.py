from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Q
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth

from accounts.mixins import DocenteOAdminMixin, SoloAdminMixin
from accounts.tasks import notificar_nota_email
from .models import Materia, Curso, Nota, Asistencia
from .forms import MateriaForm, CursoForm, NotaForm, AsistenciaForm


# ── Materias ──────────────────────────────────────────────────────────────────

class MateriaListView(LoginRequiredMixin, ListView):
    model               = Materia
    template_name       = 'academic/materia_list.html'
    context_object_name = 'materias'
    paginate_by         = 15

    def get_queryset(self):
        qs = super().get_queryset()
        q  = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class MateriaCreateView(SoloAdminMixin, CreateView):
    model         = Materia
    form_class    = MateriaForm
    template_name = 'academic/materia_form.html'
    success_url   = reverse_lazy('materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Materia creada exitosamente.')
        return super().form_valid(form)


class MateriaUpdateView(SoloAdminMixin, UpdateView):
    model         = Materia
    form_class    = MateriaForm
    template_name = 'academic/materia_form.html'
    success_url   = reverse_lazy('materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Materia actualizada.')
        return super().form_valid(form)


class MateriaDeleteView(SoloAdminMixin, DeleteView):
    model         = Materia
    template_name = 'academic/materia_confirm_delete.html'
    success_url   = reverse_lazy('materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Materia eliminada.')
        return super().form_valid(form)


# ── Cursos ────────────────────────────────────────────────────────────────────

class CursoListView(LoginRequiredMixin, ListView):
    model               = Curso
    template_name       = 'academic/curso_list.html'
    context_object_name = 'cursos'
    paginate_by         = 12

    def get_queryset(self):
        qs = super().get_queryset()
        # Estudiante solo ve los cursos en los que está inscrito
        if self.request.user.es_estudiante():
            qs = qs.filter(estudiantes=self.request.user)
        q  = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(periodo__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class CursoCreateView(SoloAdminMixin, CreateView):
    model         = Curso
    form_class    = CursoForm
    template_name = 'academic/curso_form.html'
    success_url   = reverse_lazy('curso-list')

    def form_valid(self, form):
        messages.success(self.request, 'Curso creado exitosamente.')
        return super().form_valid(form)


class CursoUpdateView(SoloAdminMixin, UpdateView):
    model         = Curso
    form_class    = CursoForm
    template_name = 'academic/curso_form.html'
    success_url   = reverse_lazy('curso-list')

    def form_valid(self, form):
        messages.success(self.request, 'Curso actualizado.')
        return super().form_valid(form)


class CursoDeleteView(SoloAdminMixin, DeleteView):
    model         = Curso
    template_name = 'academic/curso_confirm_delete.html'
    success_url   = reverse_lazy('curso-list')

    def form_valid(self, form):
        messages.success(self.request, 'Curso eliminado.')
        return super().form_valid(form)


# ── Notas ─────────────────────────────────────────────────────────────────────

class NotaListView(LoginRequiredMixin, ListView):
    model               = Nota
    template_name       = 'academic/nota_list.html'
    context_object_name = 'notas'
    paginate_by         = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('estudiante', 'materia', 'curso')
        if self.request.user.es_estudiante():
            qs = qs.filter(estudiante=self.request.user)
        elif self.request.user.es_docente():
            mis_materias = Materia.objects.filter(docente=self.request.user, activa=True)
            qs = qs.filter(materia__in=mis_materias)
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(estudiante__first_name__icontains=q) |
                Q(estudiante__last_name__icontains=q)  |
                Q(materia__nombre__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class NotaCreateView(DocenteOAdminMixin, CreateView):
    model         = Nota
    form_class    = NotaForm
    template_name = 'academic/nota_form.html'
    success_url   = reverse_lazy('nota-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)  # guarda la nota una sola vez
        notificar_nota_email(self.object)    # self.object es la nota recién creada
        messages.success(self.request, 'Nota registrada y notificación enviada.')
        return response


class NotaUpdateView(DocenteOAdminMixin, UpdateView):
    model         = Nota
    form_class    = NotaForm
    template_name = 'academic/nota_form.html'
    success_url   = reverse_lazy('nota-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Nota actualizada.')
        return super().form_valid(form)


class NotaDeleteView(SoloAdminMixin, DeleteView):
    model         = Nota
    template_name = 'academic/nota_confirm_delete.html'
    success_url   = reverse_lazy('nota-list')

    def form_valid(self, form):
        messages.success(self.request, 'Nota eliminada.')
        return super().form_valid(form)


# ── Asistencia ────────────────────────────────────────────────────────────────

class AsistenciaListView(LoginRequiredMixin, ListView):
    model               = Asistencia
    template_name       = 'academic/asistencia_list.html'
    context_object_name = 'asistencias'
    paginate_by         = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('estudiante', 'materia', 'curso')
        # Estudiante solo ve su propia asistencia
        if self.request.user.es_estudiante():
            qs = qs.filter(estudiante=self.request.user)
        elif self.request.user.es_docente():
            mis_materias = Materia.objects.filter(docente=self.request.user, activa=True)
            qs = qs.filter(materia__in=mis_materias)
        q  = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(estudiante__first_name__icontains=q) |
                Q(estudiante__last_name__icontains=q)  |
                Q(materia__nombre__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class AsistenciaCreateView(DocenteOAdminMixin, CreateView):
    model         = Asistencia
    form_class    = AsistenciaForm
    template_name = 'academic/asistencia_form.html'
    success_url   = reverse_lazy('asistencia-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Asistencia registrada.')
        return super().form_valid(form)


# ── Buscador global ───────────────────────────────────────────────────────────

class BuscadorView(DocenteOAdminMixin, ListView):
    template_name       = 'academic/buscar.html'
    context_object_name = 'estudiantes'

    def get_queryset(self):
        from accounts.models import CustomUser
        q = self.request.GET.get('q', '').strip()
        if not q:
            return CustomUser.objects.none()
        return CustomUser.objects.filter(rol='estudiante').filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)  |
            Q(email__icontains=q)
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q   = self.request.GET.get('q', '').strip()
        ctx['query']  = q
        ctx['cursos'] = Curso.objects.filter(
            Q(nombre__icontains=q) | Q(periodo__icontains=q)
        ) if q else Curso.objects.none()
        return ctx


# ── APIs JSON para Chart.js ───────────────────────────────────────────────────

@login_required
def promedios_por_materia(request):
    data = (
        Nota.objects
        .values('materia__nombre')
        .annotate(promedio=Avg('valor'))
        .order_by('materia__nombre')
    )
    return JsonResponse({
        'labels': [d['materia__nombre'] for d in data],
        'data':   [round(float(d['promedio']), 2) for d in data],
    })


@login_required
def asistencia_mensual(request):
    data = (
        Asistencia.objects
        .filter(presente=True)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    return JsonResponse({
        'labels': [d['mes'].strftime('%b %Y') for d in data],
        'data':   [d['total'] for d in data],
    })
