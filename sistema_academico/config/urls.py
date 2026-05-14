from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('accounts/',   include('accounts.urls')),
    # TODO: Juliana implementará estos includes cuando tenga sus URLs listas
    # path('academic/',   include('academic.urls')),
    # path('reports/',    include('reports.urls')),
    # path('dashboard/',  include('dashboard.urls')),
    path('',            RedirectView.as_view(url='/accounts/login/'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)