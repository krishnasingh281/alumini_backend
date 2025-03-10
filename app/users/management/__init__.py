"""
Django command to wait for the database to be available.
"""
import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

try:
    from MySQLdb import OperationalError as MySQLOpError
except ImportError:
    MySQLOpError = OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available."""

    def handle(self, *args, **options):
        """Handle the command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                connection.ensure_connection()
                db_up = True
            except (OperationalError, MySQLOpError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
