"""
WSGI config for dj110 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InventarioCitesoft.settings")

try:
	application = get_wsgi_application()
	print('INVENTARIO APP OK')
except Exception:
	print('INVENTARIO APP EXCEPTION')
	if 'mod_wsgi' in sys.modules:
		traceback.print_exc()
		os.kill(os.getpid(), signal.SIGINT)
		time.sleep(2.5)
