from django.core.management.base import BaseCommand
from django.core.management import call_command

import os


class Command(BaseCommand):
    help = "Recreate all the database stuffs from scratch"

    def handle(self, *args, **options):
        print '* reset_db'
        call_command('reset_db', router='default')
        print '* syncdb'
        call_command('syncdb', noinput=True)
        print '* migrate'
        call_command('migrate')
        fixtures_path = os.path.abspath(# build the path to the admin fixture
                os.path.join(
                    os.path.dirname(__file__),
                    '../../fixtures/admin.json')
                )
        print '* loaddata "%s"' % fixtures_path
        call_command('loaddata', fixtures_path)
