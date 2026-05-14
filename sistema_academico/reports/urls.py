from django.urls import path
from .views import ReportesView, BoletinPDFView, ActaCursoPDFView, ReporteExcelView

urlpatterns = [
    # Página principal de reportes (con filtros)
    path('',                                 ReportesView.as_view(),     name='reportes'),

    # Boletín individual PDF (?desde=YYYY-MM-DD&hasta=YYYY-MM-DD)
    path('boletin/<int:estudiante_id>/pdf/', BoletinPDFView.as_view(),   name='boletin-pdf'),

    # Acta completa de un curso en PDF
    path('acta/<int:curso_id>/pdf/',         ActaCursoPDFView.as_view(), name='acta-pdf'),

    # Excel con filtros (?desde=&hasta=&materia=&curso=)
    path('notas/excel/',                     ReporteExcelView.as_view(), name='reporte-excel'),
]
