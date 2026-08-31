from apps.posts.models import Enlace
from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.posts.forms import Comentario_form, Post_form
from apps.posts.models import Comentario, Post
from apps.tablon.models import Tablon
import os

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
    enlaces = Enlace.objects.filter(post=post)
    n_archivo = os.path.basename(str(post.archivo_img))
    context = {
        "post": post,
        "comens": comens,
        "simb": simbolo,
        "enlaces": enlaces,
        "nombre_archivo": n_archivo,
    }

    # Petición POST
    if request.method == "POST":
        # Validador de formularios
        form = Comentario_form(request.POST, post_id=post.id)
        errores_form = []
        if form.is_valid():
            id_com_resp = request.POST["id_respuesta_coment"]
            # sub_coment = None

            # En caso de que el campo de id_respuesta_coment contenga algo
            # if id_com_resp:
            #     sub_coment = Comentario.objects.get(id=id_com_resp)

            sub_coment = Comentario.objects.get(id=id_com_resp) if id_com_resp else None

            # Crea una respuesta/comentario para un post, respondiendo a otro comentario/respuesta
            Comentario.objects.create(
                contenido=request.POST["contenido_post"],
                post=post,
                sub_comentario=sub_coment,
            )
            return redirect("post_view", post.tablon.id, post.id)
        else:
            # print(form.errors)
            for i in form.errors:
                errores_form.append(form.errors[i])
            context["errores_form"] = errores_form
    return render(request, "posts/post.html", context)


# NOTA: FALTA VALIDAR EL FORMULARIO EN ESTA VISTA
# Vista para el form de respuesta de post
# def response_posting_form(request, simbolo, id_post):
#     if request.method != "POST":
#         return HttpResponse("404")
#         # print(f"{request.POST['id_respuesta_coment'] == ''}")
#         # return redirect("post_view", simbolo, id_post)

#     try:
#         post = Post.objects.get(id=id_post)
#     except Exception as e:
#         print(f"{e}")
#         return HttpResponse("404")

#     # Validador de formularios
#     form = Comentario_form(request.POST)
#     if not form.is_valid():
#         print(form.errors)
#         # context = {"errores_formulario": form.errors}
#         # return render(request, "posts/post.html", context)
#         return HttpResponse("404")

#     # Si no hay un id en el campo de id para respuesta, carga el comentario y finaliza...
#     id_com_resp = request.POST["id_respuesta_coment"]
#     if not id_com_resp:
#         # Crea una respuesta/comentario simple para un post
#         Comentario.objects.create(contenido=request.POST["contenido_post"], post=post)
#         return redirect("post_view", simbolo, id_post)

#     # Caso contrario, valida el id y relaciona los comentarios...
#     try:
#         com_resp = Comentario.objects.get(id=id_com_resp)
#     except Exception as e:
#         print(f"{e}")
#         return HttpResponse("404")
#     # Verifica que el id de comentario ingresado corresponda a un comentario del post actual
#     if com_resp.post.id != post.id:
#         print("El id de comentario no pertenece a este post.")
#         return HttpResponse("404")
#     # Crea una respuesta/comentario para un post, respondiendo a otro comentario/respuesta
#     Comentario.objects.create(
#         contenido=request.POST["contenido_post"],
#         post=post,
#         sub_comentario=com_resp,
#     )
#     return redirect("post_view", simbolo, id_post)


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

# Vista del template para postear
# def posting_view(request, simbolo):
#     context = {"simbolo": simbolo}
#     return render(request, "posts/posting_form.html", context)


# Vista para el formulario para postear
# def posting_form(request, simbolo):
#     # Para omitir peticiones que vengan por otro metodo
#     if request.method != "POST":
#         return HttpResponse("404")

#     try:
#         tablon = Tablon.objects.get(id=simbolo)
#     except Exception as e:
#         print(f"{e}")
#         return HttpResponse("404")

#     # Pasa todo el contenido del formulario al validador
#     # NOTA: En este caso se pasa el contenido del post y tambien los
#     # archivos que recibe el formulario, de lo contrario no validará el campo de imagenes.
#     form = Post_form(request.POST, request.FILES)
#     if not form.is_valid():
#         # ESTOY TENIENDO PROBLEMAS PARA PASAR EL ERROR A LA TEMPLATE PARA PODER VISUALIZARLA!!!
#         print(form.errors)
#         context = {"errores_formulario": form.errors}
#         return render(request, "tablon/tablon.html", context)
#         # return HttpResponse("404")

#     # Crea el nuevo post
#     Post.objects.create(
#         titulo=request.POST["titulo_post"],
#         contenido=request.POST["contenido_post"],
#         op_aka=request.POST["nick_OP"],
#         archivo_img=request.FILES.get(
#             "img_post"
#         ),  # ^ Debe existir el dir. 'media' en la raiz del proyecto
#         tablon=tablon,
#     )
#     # No hace falta por que el metodo create ya lo persiste
#     # Nuevo_post.save()
#     return redirect("tablon_vista", simbolo)
#     # return HttpResponse("MAL")

"""
