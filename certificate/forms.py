from django import forms
from certificate.models import Certificado, Data


class DataForm(forms.ModelForm):
    """
    Formulario de la data que se sube al servidor.
    """

    class Meta:
        model = Data
        fields = ('descripcion', 'data_zip')
        # Opcional: agregar widgets personalizados para mejor UX
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una descripción'
            }),
            'data_zip': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        # Opcional: agregar labels personalizados
        labels = {
            'descripcion': 'Descripción del archivo',
            'data_zip': 'Archivo ZIP'
        }


class CertificadoForm(forms.ModelForm):
    """
    Formulario del certificado digital que se sube al servidor.
    """

    class Meta:
        model = Certificado
        fields = ('nombre_completo', 'cedula', 'evento_curso', 'rol', 'certificado')
        # Excluir uploaded_at ya que se llena automáticamente con auto_now_add=True

        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del participante'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cédula'
            }),
            'evento_curso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del evento o curso'
            }),
            'rol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rol del participante'
            }),
            'certificado': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'  # Especificar tipos de archivo aceptados
            })
        }

        labels = {
            'nombre_completo': 'Nombre Completo',
            'cedula': 'Cédula de Identidad',
            'evento_curso': 'Evento o Curso',
            'rol': 'Rol',
            'certificado': 'Certificado Digital'
        }

        # Opcional: agregar help texts
        help_texts = {
            'cedula': 'Ingrese el número de cédula sin puntos ni espacios',
            'certificado': 'Suba el archivo del certificado en formato PDF o imagen'
        }
