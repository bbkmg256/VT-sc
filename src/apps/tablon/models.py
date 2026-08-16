from django.db import models


# Topico disponibles en el foro
class Tablon(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_tablon = models.CharField(max_length=20, null=False)
    simbolo = models.CharField(
        max_length=5, null=False
    )  # Esto es como en 4chan onda /x/ para paranormal, /b/ para random, /v/ para videojuego, etc...
