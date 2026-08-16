"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
import configparser
from pathlib import Path

from django.core.asgi import get_asgi_application


# Lectura del fichero .ini
config_ini = Path(__file__).resolve().parent.parent.parent / "setting_file.ini"
config = configparser.ConfigParser()
config.read(config_ini)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", f"core.settings.{config['SETTING_FILE']['FILE']}"
)

application = get_asgi_application()
