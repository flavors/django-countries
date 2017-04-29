from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Collect translations :)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--locales', '-c',
            dest='locales',
            help='Comma separated list of locales')

    def handle(self, **options):
        # T O D O
        pass
