"""
WSGI config for task_management_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management_project.settings')

application = get_wsgi_application()

