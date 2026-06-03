from django.db import models

class Noticias(models.Model):
    titulo = models.CharField(max_length=255),
    contenido = models.TextField(),
    imagen_url = models.URLField(blank=True, null=True),
    autor_nombre = models.CharField(max_length=100),
    autor_email = models.EmailField(),
    entidad_nombre = models.CharField(max_length=100, blank=True, null=True),
    entidad_id = models.IntegerField(blank=True, null=True),
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    editado_por_nombre = models.CharField(max_length=100, blank=True, null=True),
    editado_por_email = models.EmailField(blank=True, null=True),
    editado_por_fecha = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo}"

