from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from academic.views import promedios_por_materia, asistencia_mensual

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('accounts/',   include('accounts.urls')),
    path('academic/',   include('academic.urls')),
    path('reports/',    include('reports.urls')),
    path('dashboard/',  include('dashboard.urls')),
    path('api/promedios/',  promedios_por_materia, name='api-promedios'),
    path('api/asistencia/', asistencia_mensual,    name='api-asistencia'),
    path('',            __import__('django.views.generic', fromlist=['RedirectView'])
                        .RedirectView.as_view(url='/dashboard/'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)