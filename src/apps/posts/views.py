from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.posts.models import Comentario, Post
from apps.tablon.models import Tablon
from .forms import Post_form


"""
Las validaciones de campo deberían hacerse en JS para el navegador del usuario, así no se está
enviando una peticion alpedo y saturando el servidor.
"""


# Vista del post
def post_view(request, simbolo, id_post):
    try:
        post = Post.objects.get(id=id_post)
    except Exception as e:
        print(f"{e}")
        return HttpResponse("404")
    # Corrige la direccion URL si el tablon no corresponde con el post buscado
    if post.tablon.id != simbolo:
        return redirect("post_view", post.tablon.id, post.id)
    comens = Comentario.objects.filter(post=post)
    context = {"post": post, "comens": comens, "simb": simbolo}
    return render(request, "posts/post.html", context)


# Vista del template para postear
# def posting_view(request, simbolo):
#     context = {"simbolo": simbolo}
#     return render(request, "posts/posting_form.html", context)


# Vista para el formulario para postear
def posting_form(request, simbolo):
    # Para omitir peticiones que vengan por otro metodo
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
            Post.objects.create(
                titulo=request.POST["titulo_post"],
                contenido=request.POST["contenido_post"],
                archivo_img=request.FILES.get(
                    "img_post"
                ),  # ^ Debe existir el dir. 'media' en la raiz del proyecto
                tablon=tablon,
            )
            # No hace falta por que el metodo create ya lo persiste
            # Nuevo_post.save()
        else:
            # ESTOY TENIENDO PROBLEMAS PARA PASAR EL ERROR A LA TEMPLATE PARA PODER VISUALIZARLA!!!
            print(form.errors)
        return redirect("tablon_vista", simbolo)
        # return HttpResponse("MAL")
    return HttpResponse("404")


# NOTA: FALTA VALIDAR EL FORMULARIO EN ESTA VISTA
# Vista para el form de respuesta de post
def response_posting_form(request, simbolo, id_post):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=id_post)
        except Exception as e:
            print(f"{e}")
            return HttpResponse("404")
        # if post.tablon.id != simbolo:
        #     return HttpResponse("404")
        # Por el momento se admiten respuestas vacias xd
        # Crea una respuesta/comentario para un post
        Comentario.objects.create(contenido=request.POST["contenido_post"], post=post)
        # print("LOG: Comentario creado!")
        return redirect("post_view", simbolo, id_post)
    return HttpResponse("404")


"""

# CODIGO SIN USAR:
# Verifica que el posteo contenga al menos el título
# if not request.POST["titulo_post"].strip():
#     print("LOG: Datos vacios")
#     return redirect("tablon_vista", simbolo)
# LOG para visualizar los post
# print(f"{request.POST['titulo_post']}\n{request.POST['contenido_post']}")

    # try:
    #     comens = Comentario.objects.filter(post=post)
    #     context = {"post": post, "comens": comens, "simb": simbolo}
    #     return render(request, "posts/post.html", context)
    # except Exception as e:
    #     print(f"{e}")
    #     return HttpResponse("404")

        # print(f"{post.tablon.id} - {tablon.id}")

    # if simbolo not in ["v", "i", "a", "tp", "b"]:
    #     return HttpResponse("404")

        # Verifica que la ruta contenga el parameto correcto para un tablon valido
        if simbolo not in ["v", "i", "a", "tp", "b"]:
            return HttpResponse("404")

"""
