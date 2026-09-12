"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# import configparser
import os
from pathlib import Path

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

# Lectura de variables de entorno (.env)
DIR_BASE = Path(__file__).resolve().parent.parent.parent
load_dotenv(DIR_BASE / ".env", override=False)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"core.settings.{os.getenv('SETTING_FILE', default='settings')}",
)

application = get_asgi_application()
