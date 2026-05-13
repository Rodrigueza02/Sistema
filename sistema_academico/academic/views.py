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