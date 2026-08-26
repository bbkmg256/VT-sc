from django.db import models
from django.utils import timezone

from apps.tablon.models import Tablon


# Clase para los posteos
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    # Nick del OP
    op_aka = models.CharField(max_length=20, null=True)
    titulo = models.CharField(max_length=60, null=False)
    contenido = models.TextField(null=False)
    fecha_publicacion = models.DateField(default=timezone.localdate)
    hora_publicacion = models.TimeField(default=timezone.localtime)
    # Imagen para el post
    archivo_img = models.ImageField(upload_to="imgs", null=True)
    # Tablon/topico al que pertenece
    tablon = models.ForeignKey(Tablon, on_delete=models.CASCADE)


# Clase para los comentarios
class Comentario(models.Model):
    id = models.BigAutoField(primary_key=True)
    contenido = models.TextField(null=False)
    fecha_publicacion = models.DateField(default=timezone.localdate)
    hora_publicacion = models.TimeField(default=timezone.localtime)
    # Post al que pertenece el comentario
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Campo autoreferencial (Sub comentarios)
    sub_comentario = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, default=None
    )


# Clase para los enlaces de posteo
class Enlaces(models.Model):
    id = models.BigAutoField(primary_key=True)
    enlace = models.URLField()
    # Post relacinado al enlace (1 pos puede contener varios enlaces)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
