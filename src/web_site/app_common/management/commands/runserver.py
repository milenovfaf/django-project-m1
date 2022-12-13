from django.core.management.commands.runserver import Command as OldCommand


class Command(OldCommand):
    def check_migrations(self):
        # runserver disable check migrations for dockerfile
        pass

    def run(self, **options):
        """Run the server, using the autoreloader if needed."""
        options['use_reloader'] = False
        return super(Command, self).run(**options)




