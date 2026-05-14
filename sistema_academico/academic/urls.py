from django.urls import path
from . import views

urlpatterns = [
    # Materias
    path('materias/',                   views.MateriaListView.as_view(),      name='materia-list'),
    path('materias/nueva/',             views.MateriaCreateView.as_view(),    name='materia-create'),
    path('materias/<int:pk>/editar/',   views.MateriaUpdateView.as_view(),    name='materia-update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(),    name='materia-delete'),

    # Cursos
    path('cursos/',                     views.CursoListView.as_view(),        name='curso-list'),
    path('cursos/nuevo/',               views.CursoCreateView.as_view(),      name='curso-create'),
    path('cursos/<int:pk>/editar/',     views.CursoUpdateView.as_view(),      name='curso-update'),
    path('cursos/<int:pk>/eliminar/',   views.CursoDeleteView.as_view(),      name='curso-delete'),

    # Notas
    path('notas/',                      views.NotaListView.as_view(),         name='nota-list'),
    path('notas/nueva/',                views.NotaCreateView.as_view(),       name='nota-create'),
    path('notas/<int:pk>/editar/',      views.NotaUpdateView.as_view(),       name='nota-update'),
    path('notas/<int:pk>/eliminar/',    views.NotaDeleteView.as_view(),       name='nota-delete'),

    # Asistencia
    path('asistencia/',                 views.AsistenciaListView.as_view(),   name='asistencia-list'),
    path('asistencia/nueva/',           views.AsistenciaCreateView.as_view(), name='asistencia-create'),

    # Buscador
    path('buscar/',                     views.BuscadorView.as_view(),         name='buscar'),

    # APIs JSON para Chart.js
    path('promedios/',                  views.promedios_por_materia,          name='api-promedios'),
    path('asistencia-data/',            views.asistencia_mensual,             name='api-asistencia'),
]
