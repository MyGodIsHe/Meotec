from importlib import import_module
import os
from subprocess import call
from django.conf import settings
from django.core.management import find_commands
from django.db import models
from django.utils.translation import ugettext_lazy as _
from meotec.commands import BaseCommand
from validators import regex_repo_name, validate_git


class Manager(models.Model):
    name = models.CharField(_('display name'), max_length=50, blank=True, null=True)
    repository = models.CharField(_('repository'), max_length=255, validators=[validate_git], help_text=_('only git'))

    def __unicode__(self):
        return self.name

    def get_repo_name(self):
        return regex_repo_name.search(self.repository).group(1)

    def update(self):
        if os.path.exists(self.repository) and not os.path.exists(os.path.join(self.repository, '.git')):
            call(["rsync", "-r", "-delete", self.repository, settings.MEOTEC_MANAGERS_ROOT])
        else:
            manager_path = os.path.join(settings.MEOTEC_MANAGERS_ROOT, self.get_repo_name())
            if os.path.exists(manager_path):
                call(["cd %s; git pull" % manager_path], shell=True)
            else:
                call(["cd %s; git clone %s" % (settings.MEOTEC_MANAGERS_ROOT, self.repository)], shell=True)

    def commands(self):
        commands = []
        repo_name = self.get_repo_name()
        manager_path = os.path.join(settings.MEOTEC_MANAGERS_ROOT, repo_name)
        for command_name in find_commands(manager_path):
            module = import_module('%s.commands.%s' % (repo_name, command_name))
            for value in module.__dict__.values():
                if isinstance(value, type) and issubclass(value, BaseCommand):
                    command = value()
                    if command.title:
                        commands.append(command)
        return commands

    def commands_sorted(self):
        return sorted(self.commands(), key=lambda obj: obj.title)

    def command(self, name):
        for i in self.commands():
            if i.name == name:
                return i

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.get_repo_name()
        super(Manager, self).save(*args, **kwargs)
        self.update()

    class Meta:
        ordering = ('name',)


class Server(models.Model):
    name = models.CharField(_('display name'), max_length=50)
    hostname = models.CharField(_('hostname'), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Site(models.Model):
    domain = models.CharField(_('domain name'), max_length=100)
    name = models.CharField(_('display name'), max_length=50)
    repository = models.CharField(_('repository'), max_length=255)
    server = models.ForeignKey(Server, verbose_name=_('server'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)