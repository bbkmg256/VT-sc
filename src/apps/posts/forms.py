from django import forms
from PIL import Image  # Pillow
from django.core.exceptions import ValidationError


# Validadores personalizados #
# Validador de archivos de imagen
def validar_formato_imagen(imagen):
    # Intenta abrir la imagen y verificar su integridad
    try:
        img = Image.open(imagen)
        # Modificar esta lista para extender los formatos permitidos
        formatos = ["JPG", "JPEG", "PNG", "WEBP", "GIF"]
        if img.format not in formatos:
            raise ValidationError("Formato de imagen no valido!")
    except Exception:
        raise ValidationError("El archivo no es una imagen o está corrupto!")
    # Vuelve a setear el puntero de indexación al archivo de imagen para persistirlo,
    # sin esto, la referencia se pierde y el dato se corrompe.
    finally:
        imagen.seek(0)


# Clases de formularios #
# Formulario de posteo
class Post_form(forms.Form):
    # Campos obligatorios
    titulo_post = forms.CharField()
    contenido_post = forms.CharField()

    # Campos no obligatorios
    img_post = forms.ImageField(required=False, validators=[validar_formato_imagen])
