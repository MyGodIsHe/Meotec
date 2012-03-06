from itertools import chain
import os
from subprocess import call
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from base import entities_by_repo, commands_by_repo
from validators import regex_repo_name


class Manager(models.Model):
    name = models.CharField(_('display name'), max_length=50)
    repository = models.CharField(_('display name'), max_length=255)

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
        return commands_by_repo(self.get_repo_name())

    def commands_sorted(self):
        return sorted(self.commands(), key=lambda obj: obj.title)

    def command(self, name):
        for i in self.commands():
            if i.name == name:
                return i

    def entities(self):
        return entities_by_repo(self.get_repo_name())

    def entities_sorted(self):
        return sorted(self.entities(), key=lambda obj: obj.__class__)

    def entity(self, name):
        for i in self.entities():
            if i.name == name:
                return i

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.get_repo_name()
        super(Manager, self).save(*args, **kwargs)
        self.update()


class Node(MPTTModel):
    name = models.CharField(_('display name'), max_length=50)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    def possible_children(self):
        from base import EntityModel
        if self.content_object:
            node_class = self.content_object.__class__
            children = node_class._entity_meta.possible_children
        else:
            node_class = EntityModel
            children = []
        for cls in chain(*[m.entities()
                              for m in Manager.objects.all()]):
            if cls not in children and node_class in cls._entity_meta.possible_parents:
                children.append(cls)
        return children

    class MPTTMeta:
        order_insertion_by = ['name']