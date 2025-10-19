from django.urls import path, re_path
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from django.conf import settings
from certificate import views

urlpatterns = [
    # URL principal - búsqueda
    path('', views.buscar, name='buscar'),

    # Lista de certificados
    path('lista_certificados',
        login_required(views.ListaCertificados.as_view()),
        name='lista_certificados'),

    # Subida de archivos .zip
    path('subir_data_zip',
        login_required(views.SubirDataZip.as_view()),
        name='subir_data_zip'),

    path('subir_data_csv',
        login_required(views.SubirDataCsv.as_view()),
        name='subir_data_csv'),

    # Eliminar archivos CSV
    path('delete_csv',
        login_required(views.delete_csv),
        name='delete_csv'),

    # Gestión de certificados
    path('guardar_certificado',
        login_required(views.GuardarCertificado.as_view()),
        name='guardar_certificado'),

    path('editar_certificado/<int:pk>',
        login_required(views.EditarCertificado.as_view()),
        name='editar_certificado'),

    path('borrar_certificado/<int:pk>',
        login_required(views.BorrarCertificado.as_view()),
        name='borrar_certificado'),

    # Procesamiento de archivos
    path('descomprimir_zip',
        login_required(views.descomprimir_zip),
        name='descomprimir_zip'),

    path('insertar_data_csv',
        views.insertar_data_csv,
        name='insertar_data_csv'),

    # Búsqueda
    path('busqueda/',
        views.busqueda,
        name='busqueda'),

    # Autenticación
    path('salir',
        login_required(views.Salir.as_view()),
        name='salir'),

    # Servir archivos media (solo para desarrollo)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # Servir archivos media después de filtrar (solo para desarrollo)
    re_path(r'^busqueda/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
