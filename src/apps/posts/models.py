from django.db import models
from django.utils import timezone

from apps.tablon.models import Tablon


# Clase abstracta para entidades Post y Comentario
class Publicacion(models.Model):
    # id = models.BigAutoField(primary_key=True)
    # Nick del OP
    op_aka = models.CharField(max_length=20, default="Anónimo")
    contenido = models.TextField()
    fecha_publicacion = models.DateField(default=timezone.localdate)
    hora_publicacion = models.TimeField(default=timezone.localtime)
    # Imagen para el post
    archivo_img = models.ImageField(upload_to="imgs", null=True, blank=True)

    # Clase Meta de Django (No confundir con metaclase)
    class Meta:
        # Define que esta entidad será abstracta y no se creará una tabla en la BD
        abstract = True


# Clase para los posteos
class Post(Publicacion):
    # El campo "id"  se crea automaticamente
    # id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    # Tablon/topico al que pertenece
    tablon = models.ForeignKey(Tablon, on_delete=models.CASCADE)


# Clase para los comentarios
class Comentario(Publicacion):
    # id = models.BigAutoField(primary_key=True)
    # Post al que pertenece el comentario
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Campo autoreferencial (Sub comentarios)
    sub_comentario = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )


# Clase para los enlaces de posteo
class Enlace(models.Model):
    # id = models.BigAutoField(primary_key=True)
    enlace = models.URLField()
    # Post relacinado al enlace (1 pos puede contener varios enlaces)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    # Comentario relacionado al enlace (El mismo concepto que arriba)
    comentario = models.ForeignKey(
        Comentario, on_delete=models.CASCADE, null=True, blank=True
    )
