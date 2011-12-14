
class BaseCommand(object):
    title = ''
    args = {}

    def run(self, *args, **kwargs):
        """
        The actual logic of the command. Subclasses must implement
        this method.

        """
        raise NotImplementedError()

    @property
    def name(self):
        return self.__class__.__name__


class SiteCommand(BaseCommand):
    pass


class ServerCommand(BaseCommand):
    pass