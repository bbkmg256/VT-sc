#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import pathlib
import sys

# Agrega el proyecto a la lista de modulos importales para el entorno de python
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

"""

Esta parte con los modulos es una pija, a ver, solo, y repito SOLO!!! se debe especificar como
ruta principal de CODIGO para el proyecto django al el dir. src (trabajando con esta esquematizacion de
directorios), ya que desde ahí tanto django (y en mi caso) como los LSP empezaran a buscar modulos y leer codigo
desde ese dir padre digamos, (no desde el dir padre del proyecto, sino el dir padre donde se aloja todo el
codigo, osea src en este caso).

|   |   |   |   |   |
v   v   v   v   v   v
"""
sys.path.append(str(pathlib.Path(__file__).resolve().parent / "src"))

# NOTA: por culpa de la mierda de arriba, tengo que cambiar todas las estructura de importación en medio codigo PTM!!!!


def main():
    """Run administrative tasks."""
    # Acá no va src, por que el de dir padre del codigo
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
