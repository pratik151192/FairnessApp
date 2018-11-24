from django.core.management.base import BaseCommand, CommandError
import csv
import sys

from accounts.models import UserValues, Robots


class Command(BaseCommand):
    help = ("Output the specified model as CSV")
    args = '[ModelName]'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('ModelName')

    def handle(self, *args, **options):
        model_name = options.get('ModelName')
        if model_name == 'UserValues':
            model = UserValues
        elif model_name == 'Robots':
            model = Robots
        field_names = [f.name for f in model._meta.fields]
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
        writer.writerow(field_names)
        for instance in model.objects.all():
            writer.writerow([getattr(instance, f) for f in field_names])