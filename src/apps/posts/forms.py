from django import forms
from django.core.exceptions import ValidationError

from apps.posts.models import Comentario

# from PIL import Image  # Pillow


"""
    Aparentemente parece que no hace falta este validador
"""
# Validadores personalizados #
# Validador de archivos de imagen
# def validar_formato_imagen(imagen):
#     # Intenta abrir la imagen y verificar su integridad
#     try:
#         img = Image.open(imagen)
#         # Modificar esta lista para extender los formatos permitidos
#         formatos = ["JPG", "JPEG", "PNG", "WEBP", "GIF"]
#         if img.format not in formatos:
#             raise ValidationError("Formato de imagen no valido!")
#     except Exception as e:
#         print(e)
#         raise ValidationError("El archivo no es una imagen o está corrupto!")
#     # Vuelve a setear el puntero de indexación al archivo de imagen para persistirlo,
#     # sin esto, la referencia se pierde y el dato se corrompe.
#     finally:
#         imagen.seek(0)


# Clases de formularios #
# Formulario base
class Form_base(forms.Form):
    # Campos obligatorios
    contenido_post = forms.CharField(
        error_messages={"required": "El post/comentario no puede estar vacío."}
    )

    # Campos no obligatorios
    img_post = forms.ImageField(required=False)
    # img_post = forms.ImageField(required=False, validators=[validar_formato_imagen])
    nick_OP = forms.CharField(
        required=False,
        max_length=15,
        error_messages={
            "max_length": "El nombre de usuario es demasiado largo. (15 carácteres max.)"
        },
    )
    link_a = forms.URLField(required=False)
    link_b = forms.URLField(required=False)
    link_c = forms.URLField(required=False)


# Formulario de posteo
class Post_form(Form_base):
    # Campos obligatorios
    titulo_post = forms.CharField(
        max_length=60,
        # Mensajed de error personalziados
        error_messages={
            "required": "El post debe contener un título.",
            "max_length": "El título es demasiado largo. (60 carácteres max.)",
        },
    )


# NOTA: este formulario va a fallar por que todavía no están los formularios de pantillas diseñados correctamente, osea
# falta crear la pantilla para el contenido base de los formuarios y crear las plantillas para cada formulario, incluyendo
# el contenido base en cada uno, con eso se van a tene nombres de campos similares y esta reutilizacion de formularios
# funcionaría correctamente...
# Formulario de comentario
class Comentario_form(Form_base):
    # Campo no obligatorio
    id_respuesta_coment = forms.IntegerField(
        required=False,
        error_messages={"invalid": "Ingrese un id de comentario válido."},
    )

    # Constructor para esta clase
    def __init__(self, *args, **kwargs):
        self.post_id = kwargs.pop("post_id", None)  # Un atributo comun xd
        # Constructor de la clase padre heredada
        # (Form, ya que se modifica clean_<nombre de campo>, que pertenece a esta clase)
        super().__init__(*args, **kwargs)

    # Valida de forma personalizada el campo "id_respuesta_coment"
    def clean_id_respuesta_coment(self):
        # Obtiene el contenido del campo del formulario
        id_comentario = self.cleaned_data.get("id_respuesta_coment")
        if id_comentario:
            try:
                com_resp = Comentario.objects.get(id=id_comentario)
            except Exception as e:
                print(e)
                raise ValidationError(
                    "El id de comentario no existe o hubo problemas para encontrarlo."
                )
            # Verifica que el id de comentario ingresado corresponda a un comentario del post actual
            if com_resp.post.id != self.post_id:
                # print(f"{self.post_id}")
                raise ValidationError("El id de comentario no pertenece a este post.")
        # Siempre se debe retornar el campo del formulario, incluso si no cambia
        return id_comentario
