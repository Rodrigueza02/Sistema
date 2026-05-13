from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl
from academic.models import Nota, Asistencia
from django.db.models import Avg

class BoletinPDFView(LoginRequiredMixin, View):
    def get(self, request, estudiante_id):
        from accounts.models import CustomUser
        estudiante = CustomUser.objects.get(pk=estudiante_id)
        notas = Nota.objects.filter(estudiante=estudiante).select_related('materia')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="boletin_{estudiante.username}.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"Boletín de Notas — {estudiante.get_full_name()}", styles['Title']))
        elements.append(Paragraph(f"Generado: {__import__('datetime').date.today()}", styles['Normal']))

        tabla_data = [['Materia', 'Tipo', 'Nota', 'Fecha']]
        for n in notas:
            tabla_data.append([n.materia.nombre, n.tipo, str(n.valor), str(n.fecha)])

        tabla = Table(tabla_data, colWidths=[180, 80, 60, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#5B21B6')),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F3F0FF')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDD6FE')),
            ('FONTSIZE', (0,0), (-1,-1), 10),
        ]))
        elements.append(tabla)
        doc.build(elements)
        return response

class ReporteExcelView(LoginRequiredMixin, View):
    def get(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Notas'

        encabezados = ['Estudiante', 'Materia', 'Curso', 'Tipo', 'Nota', 'Fecha']
        for col, enc in enumerate(encabezados, 1):
            cell = ws.cell(row=1, column=col, value=enc)
            cell.font = openpyxl.styles.Font(bold=True, color='FFFFFF')
            cell.fill = openpyxl.styles.PatternFill('solid', fgColor='5B21B6')

        notas = Nota.objects.all().select_related('estudiante', 'materia', 'curso')
        for row, nota in enumerate(notas, 2):
            ws.append([
                nota.estudiante.get_full_name(),
                nota.materia.nombre,
                nota.curso.nombre,
                nota.tipo,
                float(nota.valor),
                str(nota.fecha),
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="reporte_notas.xlsx"'
        wb.save(response)
        return response