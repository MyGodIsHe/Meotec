from django.conf import settings
import global_settings


holder = settings._wrapped

# update django settings
for name, value in global_settings.__dict__.items():
    if not hasattr(holder, name) and name.isupper():
        setattr(holder, name, value)