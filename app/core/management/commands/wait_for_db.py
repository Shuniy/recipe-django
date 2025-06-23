"""
Django command to wait for the database to be ready before starting the server.
"""

import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database to be ready."""

    def handle(self, *args, **kwargs):
        """Handle the command execution."""
        self.stdout.write("Waiting for database to be ready...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is ready!"))
        self.stdout.write("You can now start the server.")
        self.stdout.write("Run 'python manage.py runserver' to start the server.")
