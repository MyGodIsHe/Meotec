import os
import sys
from django.conf import settings
from django.db.utils import DatabaseError
import global_settings
from meotec.models import Node, Manager


holder = settings._wrapped

# update django settings
for name, value in global_settings.__dict__.items():
    if not hasattr(holder, name) and name.isupper():
        setattr(holder, name, value)

if settings.MEOTEC_MANAGERS_ROOT not in sys.path:
    sys.path.append(settings.MEOTEC_MANAGERS_ROOT)

if not os.path.exists(settings.MEOTEC_MANAGERS_ROOT):
    os.makedirs(settings.MEOTEC_MANAGERS_ROOT)

try:
    if not Node.objects.count():
        Node(name='Root').save()
    INSTALLED_APPS = getattr(holder, 'INSTALLED_APPS', [])
    for m in Manager.objects.all():
        INSTALLED_APPS.append(m.get_repo_name())
    setattr(holder, 'INSTALLED_APPS', INSTALLED_APPS)
except DatabaseError:
    pass