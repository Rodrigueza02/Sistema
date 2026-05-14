from django.urls import path
from .views import BoletinPDFView, ReporteExcelView

urlpatterns = [
    path('boletin/<int:estudiante_id>/pdf/', BoletinPDFView.as_view(),  name='boletin-pdf'),
    path('notas/excel/',                     ReporteExcelView.as_view(), name='reporte-excel'),
]