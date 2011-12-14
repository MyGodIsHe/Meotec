import os
from django.conf import settings


MEOTEC_MANAGERS_ROOT = os.path.join(settings.MEDIA_ROOT, 'managers')
MEOTEC_TMP = os.path.join(settings.MEDIA_ROOT, 'tmp')