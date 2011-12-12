import os
import sys
from django.conf import settings
import global_settings


holder = settings._wrapped

# update django settings
for name, value in global_settings.__dict__.items():
    if not hasattr(holder, name) and name.isupper():
        setattr(holder, name, value)


if settings.MEOTEC_MANAGERS_ROOT not in sys.path:
    sys.path.append(os.path.dirname(settings.MEOTEC_MANAGERS_ROOT))