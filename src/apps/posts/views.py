from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.posts.models import Comentario, Post
from apps.tablon.models import Tablon


"""
Las validaciones de campo deberían hacerse en JS para el navegador del usuario, así no se está
enviando una peticion alpedo y saturando el servidor.
"""


# Vista del post
def post_view(request, simbolo, id_post):
    try:
        post = Post.objects.get(id=id_post)
        comens = Comentario.objects.filter(post=post)
        context = {"post": post, "comens": comens, "simb": simbolo}
        return render(request, "posts/post.html", context)
    except Exception as e:
        print(f"{e}")
        return HttpResponse("404")


# Vista del template para postear
def posting_view(request, simbolo):
    context = {"simbolo": simbolo}
    return render(request, "posts/posting_form.html", context)


# Vista para el formulario para postear
def posting_form(request, simbolo):
    # Diccionario de tablones
    # direc_tabs = {"v": 1}
    """
    ^ Este diccionario serviría para comprobar la direccion de procedencia del formulario,
    de modo que al cargar el post y redireccionar al tablon, se sepa con que tablon tratar.
    La idea es tratar de no repetir tanto codigo en el match de mas abajo, y resumir el fragmento
    de creacion del post (osea, la carga a BD) a una sola sentencia, donde el id del tablon al que
    se lo quiera asociar, se vea determinado por el diccionario...
    Por el momento se deja para mas adelante.
    """

    # Para omitir peticiones que vengan por otro metodo
    if request.method == "POST":
        # Verifica que el posteo contenga al menos el título
        if not request.POST["titulo_post"].strip():
            print("LOG: Datos vacios")
            return redirect("tablon_vista", simbolo)
        # LOG para visualizar los post
        # print(f"{request.POST['titulo_post']}\n{request.POST['contenido_post']}")
        # Redireciona a la vista del post
        if simbolo not in ["v", "i", "a", "tp", "b"]:
            return HttpResponse("404")
        # Crea el nuevo post
        Post.objects.create(
            titulo=request.POST["titulo_post"],
            contenido=request.POST["contenido_post"],
            archivo_img=request.FILES.get(
                "img_post"
            ),  # ^ Debe existir el dir. 'media' en la raiz del proyecto
            tablon=Tablon.objects.get(simbolo=simbolo),
        )
        # No hace falta por que el metodo create ya lo persiste
        # Nuevo_post.save()
        return redirect("tablon_vista", simbolo)
    return HttpResponse("404")


# Vista para el form de respuesta de post
def response_posting_form(request, simbolo, id_post):
    if request.method == "POST":
        # Por el momento se admiten respuestas vacias xd
        # Crea una respuesta/comentario para un post
        Comentario.objects.create(
            contenido=request.POST["contenido_post"], post=Post.objects.get(id=id_post)
        )
        print("LOG: Comentario creado!")
        return redirect("post_view", simbolo, id_post)
    return HttpResponse("404")
