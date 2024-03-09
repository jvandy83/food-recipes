import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        max_retries = 10
        retries = 0
        
        while retries < max_retries:
            try:
                self.check(databases=['default'])
                self.stdout.write(self.style.SUCCESS('Database available!'))
                return  # Exit the function once the database is available
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                retries += 1
                time.sleep(1)

        self.stdout.write(self.style.ERROR('Database still unavailable after retries.'))
