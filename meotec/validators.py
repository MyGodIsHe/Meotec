import os
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


RE_HOSTNAME = str(
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
)

regex_ssh = re.compile(r'^[\w\.\-]+@%s:[\w\.\-]+$' % RE_HOSTNAME, re.IGNORECASE)

regex_url = re.compile(
    r'^(?:http|ftp|git)s?://' # http:// or https://
    + RE_HOSTNAME +
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

regex_repo_name = re.compile(r'.*[:/]([\w\-]+)(?:\.git)?/?$', re.IGNORECASE)


def validate_git(value):
    if regex_ssh.match(value) or regex_url.match(value):
        return
    if os.path.exists(value):
        return
    raise ValidationError(_('%s is not a valid git repository' % value))