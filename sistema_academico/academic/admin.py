from django.contrib import admin
from .models import Materia, Curso, Nota, Asistencia


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display  = ('codigo', 'nombre', 'creditos', 'docente', 'activa')
    list_filter   = ('activa', 'creditos')
    search_fields = ('nombre', 'codigo')
    list_editable = ('activa',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display   = ('nombre', 'periodo', 'año', 'activo_display')
    list_filter    = ('año', 'periodo')
    search_fields  = ('nombre',)
    filter_horizontal = ('materias', 'estudiantes')

    @admin.display(boolean=True, description='Activo')
    def activo_display(self, obj):
        return obj.estudiantes.exists()


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'materia', 'curso', 'tipo', 'valor', 'fecha')
    list_filter   = ('tipo', 'fecha', 'materia')
    search_fields = ('estudiante__username', 'estudiante__first_name', 'estudiante__last_name')
    date_hierarchy = 'fecha'


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'materia', 'curso', 'fecha', 'presente')
    list_filter   = ('presente', 'fecha', 'materia')
    search_fields = ('estudiante__username', 'estudiante__first_name', 'estudiante__last_name')
    date_hierarchy = 'fecha'
