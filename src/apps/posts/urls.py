from django.urls import path
from . import views

urlpatterns = [
    path(
        "post/<int:id_post>", views.post_view, name="post_view"
    ),  # ^ Esta ruta debe llevar el id del post
    # path("post/nuevo/form", views.posting_form, name="posting_form"),
    # path(
    #     "post/<int:id_post>/nueva_respuesta/form",
    #     views.response_posting_form,
    #     name="response_posting_form",
    # ),
    # path("post/nuevo/", views.posting_view, name="posting_view"),
    # path("post/eliminar/<int:id>"),
]
