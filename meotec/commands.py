
class BaseCommand(object):
    title = ''
    args = {}

    def run(self, *args, **kwargs):
        """
        The actual logic of the command. Subclasses must implement
        this method.

        """
        raise NotImplementedError()


class SiteCommand(BaseCommand):
    pass


class ServerCommand(BaseCommand):
    pass