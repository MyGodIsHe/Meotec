import os
import os.path
from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import LazyObject
from django.utils.importlib import import_module


class BaseCommand(object):
    title = ''
    args = {}
    valid_entities = ()

    @classmethod
    def can_run(cls, node):
        return node.__class__ in cls.valid_entities

    @classmethod
    def run(cls, *args, **kwargs):
        """
        The actual logic of the command. Subclasses must implement
        this method.

        """
        raise NotImplementedError()


class EntityOptions(object):
    """
    Options class for Entity models. Use this as an inner class called ``EntityMeta``::

        class MyModel(EntityModel):
            class EntityMeta:
                possible_parents = (EntityModel,)
                possible_children = ('base_manager.Site',)
    """

    def __init__(self, initial=None, **kwargs):
        # Override defaults with options provided
        opts = [
            ('possible_parents', ()),
            ('possible_children', ()),
        ]
        if initial:
            opts.extend(initial.__dict__.items())
        opts.extend(kwargs.items())

        for key, value in opts:
            setattr(self, key, value)

        self.possible_parents = tuple(get_class_by_path(cls) if isinstance(cls, basestring) else cls
                                      for cls in self.possible_parents)
        self.possible_children = tuple(get_class_by_path(cls) if isinstance(cls, basestring) else cls
                                       for cls in self.possible_children)

    def __iter__(self):
        return iter([(k, v) for (k, v) in self.__dict__.items() if not k.startswith('_')])


class LazyEntityOptions(LazyObject):

    def __init__(self, *args, **kwargs):
        self.__dict__['_args'] = args
        self.__dict__['_kwargs'] = kwargs
        super(LazyEntityOptions, self).__init__()

    def _setup(self):
        self._wrapped = EntityOptions(*self.__dict__['_args'], **self.__dict__['_kwargs'])


class EntityModelBase(ModelBase):

    def __new__(cls, class_name, bases, class_dict):
        """
        Create subclasses of EntityModel.
        """
        EntityMeta = class_dict.pop('EntityMeta', None)
        if not EntityMeta:
            class EntityMeta:
                pass

        class_dict['_entity_meta'] = LazyEntityOptions(EntityMeta)
        return super(EntityModelBase, cls).__new__(cls, class_name, bases, class_dict)


class EntityModel(models.Model):
    __metaclass__ = EntityModelBase

    class Meta:
        abstract = True

    @classmethod
    def class_path(cls):
        return '%s.%s' %(cls.__module__, cls.__name__)


def get_class_by_path(class_path):
    path = class_path.split('.')
    module = import_module('.'.join(path[:-1]))
    return getattr(module, path[-1])


def find_modules(*args):
    """
    Given a path to a management directory, returns a list of all the module
    names that are available.

    Returns an empty list if no modules are defined.
    """
    module_dir = os.path.join(*args)
    try:
        return [f[:-3] for f in os.listdir(module_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []


def entities_by_repo(repo_name):
    module = import_module('%s.models' % repo_name)
    return [entity
            for entity in module.__dict__.values()
            if isinstance(entity, type) and
               entity != EntityModel and
               issubclass(entity, EntityModel)]


def commands_by_repo(repo_name):
    commands = []
    manager_path = os.path.join(settings.MEOTEC_MANAGERS_ROOT, repo_name)
    for name in find_modules(manager_path, 'commands'):
        module = import_module('.'.join([repo_name, 'commands', name]))
        for command in module.__dict__.values():
            if isinstance(command, type) and issubclass(command, BaseCommand):
                if command.title:
                    commands.append(command)
    return commands