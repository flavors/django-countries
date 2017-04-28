import os

from django.core.management import call_command
from ._base_dumper import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Load fixtures'

    def handle(self, **options):
        for root, subdirs, files in os.walk(self.rootdir):
            for fixture in files:
                call_command('loaddata', os.path.join(
                    root.split('fixtures/')[1], fixture))
