from django import forms
from fabric.context_managers import settings
from fabric.operations import sudo
from meotec.commands import ServerCommand
from django.utils.translation import ugettext_lazy as _


class MySqlCommand(ServerCommand):
    title= _('MySql')
    help = _("V init script")
    args = {
        'command': forms.ChoiceField((
            ('status', _('status')),
            ('start', _('start')),
            ('stop', _('stop')),
            ('restart', _('restart')),
            ('reload', _('reload')),
            ('force-reload', _('force-reload')),
        )),
    }

    def run(self, server, kwargs):
        with settings(host_string=server.hostname):
            return sudo("service mysql %s" % kwargs['command'])


class MemcachedCommand(ServerCommand):
    title= _('Memcached')
    help = _("V init script")
    args = {
        'command': forms.ChoiceField((
            ('start', _('start')),
            ('stop', _('stop')),
            ('restart', _('restart')),
            ('force-reload', _('force-reload')),
            ('status', _('status')),
        )),
    }

    def run(self, server, kwargs):
        with settings(host_string=server.hostname):
            return sudo("service memcached %s" % kwargs['command'])


class NginxCommand(ServerCommand):
    title= _('Nginx')
    help = _("V init script")
    args = {
        'command': forms.ChoiceField((
            ('start', _('start')),
            ('stop', _('stop')),
            ('restart', _('restart')),
            ('reload', _('reload')),
            ('force-reload', _('force-reload')),
            ('configtest', _('configtest')),
            ('status', _('status')),
        )),
    }

    def run(self, server, kwargs):
        with settings(host_string=server.hostname):
            return sudo("service nginx %s" % kwargs['command'])