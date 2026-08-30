import random as rd

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static

from apps.posts.forms import Post_form
from apps.posts.models import Enlace, Post
from apps.tablon.models import Tablon


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
    nombre_tablon = None
    form = None

    # Identifica el tablo a ingresar
    match simbolo:
        case "v":
            nombre_tablon = "Videojuegos"
        case "i":
            nombre_tablon = "Internet"
        case "a":
            nombre_tablon = "Animé"
        case "tp":
            nombre_tablon = "Tecnología y programación"
        case "b":
            nombre_tablon = "Random"
        case _:
            return HttpResponse("404")

    # return HttpResponse("MAL")

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
        Post.objects.filter(tablon=simbolo)  # Como un WHERE
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

    # Petición POST
    if request.method == "POST":
        try:
            tablon = Tablon.objects.get(id=simbolo)
        except Exception as e:
            print(f"{e}")
            return HttpResponse("404")

        # Pasa todo el contenido del formulario al validador
        # NOTA: En este caso se pasa el contenido del post y tambien los
        # archivos que recibe el formulario, de lo contrario no validará el campo de imagenes.
        form = Post_form(request.POST, request.FILES)
        if form.is_valid():
            # Crea el nuevo post
            # post = Post.objects.create(
            #     titulo=request.POST["titulo_post"],
            #     contenido=request.POST["contenido_post"],
            #     archivo_img=request.FILES.get(
            #         "img_post"
            #     ),  # ^ Debe existir el dir. 'media' en la raiz del proyecto
            #     tablon=tablon,
            # )

            # No es la mejor manera, pero momentaneamente safa :9
            # Crea el nuevo post
            post = Post(
                titulo=request.POST["titulo_post"],
                contenido=request.POST["contenido_post"],
                archivo_img=request.FILES.get(
                    "img_post"
                ),  # ^ Debe existir el dir. 'media' en la raiz del proyecto
                tablon=tablon,
            )
            if request.POST["nick_OP"]:
                post.op_aka = request.POST["nick_OP"]
            post.save()

            # Persiste el link/enlace agregado si existe
            if request.POST["link_post"]:
                Enlace.objects.create(enlace=request.POST["link_post"], post=post)
        else:
            errores_form = []
            for i in form.errors:
                errores_form.append(form.errors[i])

            context["errores_form"] = errores_form
            print(form.errors)
            print(context)
    return render(request, "tablon/tablon.html", context)
