
"""
WSGI config for humain project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys
from evaluacion import settings

path = settings.PATH
if path not in sys.path:
        sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evaluacion.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
