from django import forms
from accounts.models import CustomUser
from .models import Materia, Curso, Nota, Asistencia

CSS = 'w-full px-4 py-2.5 rounded-2xl border-2 border-lavender bg-white text-sm font-semibold focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all'

# Querysets reutilizables
def qs_estudiantes():
    return CustomUser.objects.filter(rol='estudiante', activo=True).order_by('last_name', 'first_name')

def qs_docentes():
    return CustomUser.objects.filter(rol='docente', activo=True).order_by('last_name', 'first_name')


class MateriaForm(forms.ModelForm):
    class Meta:
        model  = Materia
        fields = ['nombre', 'codigo', 'descripcion', 'docente', 'creditos', 'activa']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo docentes activos en el selector
        self.fields['docente'].queryset = qs_docentes()
        self.fields['docente'].empty_label = '— Sin asignar —'
        for f in self.fields.values():
            if not isinstance(f.widget, forms.CheckboxInput):
                f.widget.attrs['class'] = CSS


class CursoForm(forms.ModelForm):
    class Meta:
        model  = Curso
        fields = ['nombre', 'año', 'periodo', 'materias', 'estudiantes']
        widgets = {
            'materias':    forms.CheckboxSelectMultiple(),
            'estudiantes': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo estudiantes activos en el selector
        self.fields['estudiantes'].queryset = qs_estudiantes()
        for name, field in self.fields.items():
            if name not in ('materias', 'estudiantes'):
                field.widget.attrs['class'] = CSS


class NotaForm(forms.ModelForm):
    class Meta:
        model  = Nota
        fields = ['estudiante', 'materia', 'curso', 'valor', 'tipo', 'observacion']

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario antes de llamar a super() para no pasarlo a ModelForm
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.es_docente():
            # Solo las materias que dicta este docente
            mis_materias = Materia.objects.filter(docente=self.user, activa=True)
            self.fields['materia'].queryset = mis_materias

            # Solo los cursos que contienen al menos una de sus materias
            from .models import Curso as CursoModel
            self.fields['curso'].queryset = CursoModel.objects.filter(
                materias__in=mis_materias
            ).distinct()

            # Solo los estudiantes inscritos en esos cursos
            from accounts.models import CustomUser as CU
            estudiantes_ids = CursoModel.objects.filter(
                materias__in=mis_materias
            ).values_list('estudiantes', flat=True).distinct()
            self.fields['estudiante'].queryset = CU.objects.filter(
                pk__in=estudiantes_ids, activo=True
            ).order_by('last_name', 'first_name')
        else:
            self.fields['estudiante'].queryset = qs_estudiantes()

        self.fields['estudiante'].empty_label = '— Seleccionar estudiante —'
        self.fields['materia'].empty_label    = '— Seleccionar materia —'
        self.fields['curso'].empty_label      = '— Seleccionar curso —'
        for f in self.fields.values():
            f.widget.attrs['class'] = CSS

    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if valor < 0 or valor > 5:
            raise forms.ValidationError('La nota debe estar entre 0.0 y 5.0')
        return valor


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model  = Asistencia
        fields = ['estudiante', 'materia', 'curso', 'fecha', 'presente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': CSS}),
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario antes de llamar a super() para no pasarlo a ModelForm
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.es_docente():
            # Solo las materias que dicta este docente
            mis_materias = Materia.objects.filter(docente=self.user, activa=True)
            self.fields['materia'].queryset = mis_materias

            # Solo los cursos que contienen al menos una de sus materias
            from .models import Curso as CursoModel
            self.fields['curso'].queryset = CursoModel.objects.filter(
                materias__in=mis_materias
            ).distinct()

            # Solo los estudiantes inscritos en esos cursos
            from accounts.models import CustomUser as CU
            estudiantes_ids = CursoModel.objects.filter(
                materias__in=mis_materias
            ).values_list('estudiantes', flat=True).distinct()
            self.fields['estudiante'].queryset = CU.objects.filter(
                pk__in=estudiantes_ids, activo=True
            ).order_by('last_name', 'first_name')
        else:
            self.fields['estudiante'].queryset = qs_estudiantes()

        self.fields['estudiante'].empty_label = '— Seleccionar estudiante —'
        self.fields['materia'].empty_label    = '— Seleccionar materia —'
        self.fields['curso'].empty_label      = '— Seleccionar curso —'
        for name, field in self.fields.items():
            if name not in ('fecha', 'presente'):
                field.widget.attrs['class'] = CSS
