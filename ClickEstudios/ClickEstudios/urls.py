
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404



urlpatterns = [
    path('' , include('Estudios.urls')),
    path('asistente/', include('Asistente.urls')),
    path('admin/', admin.site.urls),
    path('accouns/', include('Accounts.urls')),
    path('accounts/', include('allauth.urls')),
]

handler404 = 'Estudios.views.Status404'
handler404 = 'Estudios.views.error_redirect_view'
handler500 = 'Estudios.views.error_redirect_view'
handler403 = 'Estudios.views.error_redirect_view'
handler400 = 'Estudios.views.error_redirect_view'


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)