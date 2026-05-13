from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Avg, Q
from django.contrib import messages
from accounts.mixins import DocenteOAdminMixin, SoloAdminMixin
from .models import Materia, Curso, Nota, Asistencia
from .forms import MateriaForm, NotaForm, AsistenciaForm

# ── Materias ──────────────────────────────────────────────
class MateriaListView(DocenteOAdminMixin, ListView):
    model = Materia
    template_name = 'academic/materia_list.html'
    context_object_name = 'materias'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q))
        return qs

class MateriaCreateView(SoloAdminMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'academic/materia_form.html'
    success_url = reverse_lazy('materia-list')

    def form_valid(self, form):
        messages.success(self.request, 'Materia creada exitosamente.')
        return super().form_valid(form)

class MateriaUpdateView(SoloAdminMixin, UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'academic/materia_form.html'
    success_url = reverse_lazy('materia-list')

class MateriaDeleteView(SoloAdminMixin, DeleteView):
    model = Materia
    template_name = 'academic/materia_confirm_delete.html'
    success_url = reverse_lazy('materia-list')

# ── Notas ─────────────────────────────────────────────────
class NotaCreateView(DocenteOAdminMixin, CreateView):
    model = Nota
    form_class = NotaForm
    template_name = 'academic/nota_form.html'
    success_url = reverse_lazy('nota-list')

    def form_valid(self, form):
        nota = form.save()
        # Enviar email al guardar nota
        from .tasks import notificar_nota_email
        notificar_nota_email(nota)
        messages.success(self.request, 'Nota registrada y notificación enviada.')
        return super().form_valid(form)

# ── Dashboard data (API JSON para Chart.js) ───────────────
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
        'data':   [float(d['promedio']) for d in data],
    })

@login_required
def asistencia_mensual(request):
    from django.db.models.functions import TruncMonth
    data = (
        Asistencia.objects
        .filter(presente=True)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=models.Count('id'))
        .order_by('mes')
    )
    return JsonResponse({
        'labels': [d['mes'].strftime('%b %Y') for d in data],
        'data':   [d['total'] for d in data],
    })
    
    # Agregar estas clases al views.py de academic que ya tenías

class CursoListView(DocenteOAdminMixin, ListView):
    model = Curso
    template_name = 'academic/curso_list.html'
    context_object_name = 'cursos'

class CursoCreateView(SoloAdminMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'academic/curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoUpdateView(SoloAdminMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'academic/curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoDeleteView(SoloAdminMixin, DeleteView):
    model = Curso
    template_name = 'academic/curso_confirm_delete.html'
    success_url = reverse_lazy('curso-list')

class NotaListView(LoginRequiredMixin, ListView):
    model = Nota
    template_name = 'academic/nota_list.html'
    context_object_name = 'notas'

    def get_queryset(self):
        qs = super().get_queryset().select_related('estudiante', 'materia', 'curso')
        # Los estudiantes solo ven sus propias notas
        if self.request.user.es_estudiante():
            qs = qs.filter(estudiante=self.request.user)
        return qs

class NotaUpdateView(DocenteOAdminMixin, UpdateView):
    model = Nota
    form_class = NotaForm
    template_name = 'academic/nota_form.html'
    success_url = reverse_lazy('nota-list')

class NotaDeleteView(SoloAdminMixin, DeleteView):
    model = Nota
    template_name = 'academic/nota_confirm_delete.html'
    success_url = reverse_lazy('nota-list')

class AsistenciaListView(DocenteOAdminMixin, ListView):
    model = Asistencia
    template_name = 'academic/asistencia_list.html'
    context_object_name = 'asistencias'

class AsistenciaCreateView(DocenteOAdminMixin, CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'academic/asistencia_form.html'
    success_url = reverse_lazy('asistencia-list')

class BuscadorView(LoginRequiredMixin, ListView):
    template_name = 'academic/buscar.html'
    context_object_name = 'resultados'

    def get_queryset(self):
        from django.db.models import Q
        from accounts.models import CustomUser
        q = self.request.GET.get('q', '').strip()
        if not q:
            return []
        estudiantes = CustomUser.objects.filter(
            rol='estudiante'
        ).filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
        )
        cursos = Curso.objects.filter(Q(nombre__icontains=q) | Q(periodo__icontains=q))
        return {'estudiantes': estudiantes, 'cursos': cursos, 'query': q}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx