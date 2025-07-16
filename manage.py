# Cambios realizados:
#       * se arreglo problema de búsqueda global.
#       * se incorporo activos (monitores, audio, tablets).
#       * se incorporaron activos nuevos en la template de home, tambien se incorporo bodega ADR y azotea.
#       * se incorporó los activos nuevos en la barra lateral.
#       * se corrigió problema de envios de correos.
#       * se añadió barra de búsqueda dentro del fitro de la búsqueda.
#       * se modifico el parámetro "marcas" que el usuario escriba un marca en cuestión.
#       * se modifico base de datos para incorporar todas las funcionalidades anteriores y se actualizó la base de datos con los ultimos activos de la bdc.
#       * se incorporó en los detalles del activo un historial de cambios.
#     fecha: 20/06/2025
#     Por> Nicolas Araya, Felipe Frez 

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()




