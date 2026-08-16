"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import configparser
from pathlib import Path

from django.core.wsgi import get_wsgi_application


# Lectura del fichero .ini
config_ini = Path(__file__).resolve().parent.parent.parent / "setting_file.ini"
config = configparser.ConfigParser()
config.read(config_ini)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", f"core.settings.{config['SETTING_FILE']['FILE']}"
)

application = get_wsgi_application()
