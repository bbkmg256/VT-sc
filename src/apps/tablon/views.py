from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
import random as rd

# from .models import Tablon
from apps.posts.models import Post


def banner_aleatorio():
    """
    El directorio 'statics' tiene que crearse en la raiz del proyecto y dentro debe haber
    un directorio llamado 'banners', dentro de ese dir. estarán los banneres...
    """
    cant_banners = 5
    banner = rd.randint(1, cant_banners)
    return static(f"banners/{banner}.png")
    # return static(f"banners/{1}.png")


def tablon_vista(request, simbolo):
    # Selecciona un banner aleatorio para la vista
    banner = banner_aleatorio()
    id_tablon = None
    nombre_tablon = None

    # Identifica el tablo a ingresar
    match simbolo:
        case "v":
            id_tablon = 1
            nombre_tablon = "Videojuegos"
        case "i":
            id_tablon = 2
            nombre_tablon = "Internet"
        case "a":
            id_tablon = 3
            nombre_tablon = "Animé"
        case "tp":
            id_tablon = 4
            nombre_tablon = "Tecnología y programación"
        case "b":
            id_tablon = 5
            nombre_tablon = "Random"
        case _:
            return HttpResponse("404")

    # Se ordena el queryset por fecha de publicación
    # post_data = Post.objects.filter(tablon=1).order_by(
    #     # El - (guión) le dice a django que la organizacion será de forma descendente
    #     "-fecha_publicacion",
    #     "-hora_publicacion",
    # )

    """
    Esta consulta trae los items realizando un filtrado y generando un campo especifico que agrupa el numero de objetos que tiene relacionado cada objeto del modelo especifo.
    Como una especia de GROUP BY en SQL
    """
    post_data = (
        Post.objects.filter(tablon=id_tablon)  # Como un WHERE
        .annotate(total_respuestas=Count("comentario"))  # Como un GROUP BY
        .order_by(  # Como un ORDER BY xd
            # El - (guión) le dice a django que la organizacion será de forma descendente
            "-fecha_publicacion",
            "-hora_publicacion",
        )
    )

    # print(type(post_data))
    # print(len(post_data))
    # print(post_data.first().id)
    context = {
        "post_data": post_data,
        "simb": simbolo,
        "nombre_tablon": nombre_tablon,
        "banner": banner,
    }
    return render(request, "tablon/tablon.html", context)
