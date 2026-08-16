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


def tablon_vista(request, simbolo):
    # Selecciona un banner aleatorio para la vista
    banner = banner_aleatorio()

    # Identifica el tablo a ingresar
    match simbolo:
        case "v":
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
                Post.objects.filter(tablon=1)  # Como un WHERE
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
                "banner": banner,
            }
            return render(request, "tablon/videojuegos.html", context)
        case "i":
            return HttpResponse("Todavía en desarrollo, vuelva más tarde")
        case "a":
            return HttpResponse("Todavía en desarrollo, vuelva más tarde")
        case "tp":
            return HttpResponse("Todavía en desarrollo, vuelva más tarde")
        case "b":
            return HttpResponse("Todavía en desarrollo, vuelva más tarde")
        case _:
            return HttpResponse("404")
