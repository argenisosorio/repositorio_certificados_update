from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from certificate.models import Certificado, Data
from certificate.forms import CertificadoForm, DataForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
import os
import csv
from django.db.models import Max


class SubirDataZip(SuccessMessageMixin, CreateView):
    """
    Clase que permite subir la data .zip en el servidor.
    """
    model = Data
    form_class = DataForm
    template_name = "certificate/subir_data_zip.html"
    success_url = reverse_lazy('certificate:subir_data_zip')
    success_message = "La data .zip se guardó con éxito"

    def post(self, request, *args, **kwargs):
        self.object = None

        return super().post(request, *args, **kwargs)


class SubirDataCsv(SuccessMessageMixin, CreateView):
    """
    Clase que permite subir la data .csv en el servidor.
    """
    model = Data
    form_class = DataForm
    template_name = "certificate/subir_data_csv.html"
    success_url = reverse_lazy('certificate:subir_data')
    success_message = "La data se guardó con éxito"

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


def descomprimir_zip(request):
    """
    Función que sirve para descomprimir y luego borrar el .zip adjuntado
    anteriormente.
    """
    original_dir = os.getcwd()  # Guardar el directorio actual

    try:
        os.chdir(settings.MEDIA_ROOT)  # Cambiarse al directorio media
        os.system("unzip -o *.zip")  # Descomprimir todos los .zip (sobrescribir)
        os.system("rm -f *.zip")  # Remover todos los .zip del directorio
    finally:
        os.chdir(original_dir)  # Cambiarse al directorio raíz del proyecto

    messages.success(request, '¡Se descomprimió el .zip con éxito y luego se borró el .zip!')
    return render(request, 'certificate/home.html')


def insertar_csv(request):
    """
    Función que permite insertar la data .csv en la base de datos.
    """
    original_dir = os.getcwd()

    try:
        # Ejecutar el script en bash pasando los parámetros necesarios
        exit_code = os.system(
            f"bash insert_csv.sh {settings.MEDIA_ROOT} {settings.DATABASES['default']['NAME']}"
        )

        if exit_code == 0:
            messages.success(request, '¡Se insertó la data .csv correctamente!')
        else:
            messages.error(request, 'Error al insertar la data .csv')
    finally:
        os.chdir(original_dir)

    return render(request, 'certificate/home.html')


def insertar_data_csv(request):
    """
    Función que permite insertar los datos del fichero CSV en la base de datos.
    """
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'data_final.csv')

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as listado:
            datos = csv.reader(listado, delimiter=',')

            for row in datos:
                if len(row) >= 6:  # Verificar que la fila tenga suficientes columnas
                    nombre_completo = row[0]
                    cedula = row[1]
                    evento_curso = row[2]
                    rol = row[3]
                    certificado = row[4]
                    uploaded_at = row[5]

                    Certificado.objects.create(
                        nombre_completo=nombre_completo,
                        cedula=cedula,
                        evento_curso=evento_curso,
                        rol=rol,
                        certificado=certificado,
                        uploaded_at=uploaded_at
                    )

        # Ejecutar script de limpieza
        original_dir = os.getcwd()
        os.system(f"bash delete_csv.sh {settings.MEDIA_ROOT} {settings.DATABASES['default']['NAME']}")
        os.chdir(original_dir)

        messages.success(request, '¡Se insertó la data .csv correctamente!')

    except FileNotFoundError:
        messages.error(request, 'No se encontró el archivo data_final.csv')
    except Exception as e:
        messages.error(request, f'Error al procesar el CSV: {str(e)}')

    return render(request, 'certificate/home.html')


def delete_csv(request):
    """
    Elimina todos los archivos .csv de la carpeta MEDIA_ROOT del proyecto.
    
    :param request: HttpRequest object
    :return: HttpResponse con mensaje y redirección a template
    :author: Ing. Argenis Osorio <aosorio@cenditel.gob.ve>
    """
    original_dir = os.getcwd()

    try:
        exit_code = os.system(
            f"bash delete_csv.sh {settings.MEDIA_ROOT} {settings.DATABASES['default']['NAME']}"
        )
        
        if exit_code == 0:
            messages.success(request, '¡Se eliminaron los archivos .csv correctamente!')
        else:
            messages.error(request, 'Error al eliminar los archivos .csv')
    finally:
        os.chdir(original_dir)

    return render(request, 'certificate/home.html')


def formato_fecha(request):
    """
    Función que cambia el formato de hora y fecha de python
    """
    uploaded_at = datetime.now()
    fecha_hora = uploaded_at.strftime("%d-%m-%Y %H:%M")
    return render(request, 'certificate/lista_certificados.html', {'uploaded_at': fecha_hora})


class GuardarCertificado(SuccessMessageMixin, CreateView):
    """
    Clase que permite guardar los certificados en /media.
    """
    model = Certificado
    form_class = CertificadoForm
    template_name = "certificate/guardar_certificado.html"
    success_url = reverse_lazy('certificate:buscar')
    success_message = "Se guardó el certificado con éxito"


class ListaCertificados(ListView):
    """
    Clase que permite listar los certificados registrados.
    """
    model = Certificado
    template_name = "certificate/lista_certificados.html"
    ordering = ['-uploaded_at']  # Ordenar por fecha de subida descendente
    paginate_by = 20  # Opcional: agregar paginación


class EditarCertificado(SuccessMessageMixin, UpdateView):
    """
    Clase que permite editar los certificados registrados.
    """
    template_name = "certificate/editar_certificado.html"
    form_class = CertificadoForm
    model = Certificado
    success_message = "Se actualizó la información con éxito"
    success_url = reverse_lazy('certificate:lista_certificados')


class BorrarCertificado(SuccessMessageMixin, DeleteView):
    """
    Clase que permite borrar los certificados.
    """
    model = Certificado
    template_name = "certificate/certificado_confirm_delete.html"  # Especificar template
    success_message = "Se eliminó la información con éxito"
    success_url = reverse_lazy('certificate:lista_certificados')


def buscar(request):
    """
    Función que muestra la plantilla con el formulario de búsqueda.
    """
    return render(request, 'certificate/home.html')


def busqueda(request):
    """
    Función que permite hacer el query con los certificados ya filtrados.
    """
    q = request.GET.get('q', '').strip()

    if not q:
        messages.warning(request, 'Por favor introduce una cédula de identidad.')
        return render(request, 'certificate/home.html')
    
    # Agrupar los certificados por los campos que definen la unicidad y
    # encontrar el id del certificate más reciente en cada grupo.
    certificados_unicos = Certificado.objects.filter(cedula=q).values(
        'nombre_completo',
        'evento_curso',
        'rol'
    ).annotate(max_id=Max('id'))

    # Extraer los IDs de los certificates más recientes.
    ids_unicos = [c['max_id'] for c in certificados_unicos]

    # Obtener los objetos completos usando los IDs únicos.
    certificados = Certificado.objects.filter(id__in=ids_unicos).order_by('-uploaded_at')

    if certificados:
        return render(request, 'certificate/home.html', {
            'certificados': certificados,
            'query': q
        })
    else:
        messages.info(request, 'No se encontró ningún certificado.')
        return render(request, 'certificate/home.html')


class Salir(View):
    """
    Clase que permite cerrar la sesión de usuario.
    """

    def get(self, request):
        """
        Método que redirecciona cuando se cierra la sesión.
        """
        logout(request)
        return redirect('/')
