from django import forms
from .models import Materia, Curso, Nota, Asistencia

CSS = 'w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-500'

class MateriaForm(forms.ModelForm):
    class Meta:
        model  = Materia
        fields = ['nombre', 'codigo', 'descripcion', 'docente', 'creditos', 'activa']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
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
        for name, field in self.fields.items():
            if name not in ('materias', 'estudiantes'):
                field.widget.attrs['class'] = CSS

class NotaForm(forms.ModelForm):
    class Meta:
        model  = Nota
        fields = ['estudiante', 'materia', 'curso', 'valor', 'tipo', 'observacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'fecha':
                field.widget.attrs['class'] = CSS