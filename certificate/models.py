# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str


class Data(models.Model):
    """
    Modelo de la data que se sube al servidor.
    """
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    data_zip = models.FileField(upload_to='uploads/data_zips/', blank=True, null=True)

    def __str__(self):
        return force_str(self.descripcion)

    class Meta:
        # Opcional: agregar nombres más descriptivos para el admin
        verbose_name = "Datos"
        verbose_name_plural = "Datos"


class Certificado(models.Model):
    """
    Modelo del certificado digital que se sube al servidor.
    """
    nombre_completo = models.CharField(max_length=255, blank=True, null=True)
    cedula = models.CharField(max_length=255, blank=True, null=True)
    evento_curso = models.CharField(max_length=255, blank=True, null=True)
    rol = models.CharField(max_length=255, blank=True, null=True)
    certificado = models.FileField(upload_to='uploads/certificados/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('certificate:editar_certificado', kwargs={'pk': self.pk})

    def __str__(self):
        return force_str(self.cedula) if self.cedula else force_str(self.nombre_completo)

    class Meta:
        # Nombre de la tabla en la base de datos.
        db_table = 'registro_certificado'
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        # Opcional: agregar índices para mejorar performance
        indexes = [
            models.Index(fields=['cedula']),
            models.Index(fields=['uploaded_at']),
        ]
        # Ordenamiento por defecto
        ordering = ['-uploaded_at']
