import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import data from json file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                mymodel = Ingredient()
                mymodel.name = item['name']
                mymodel.measurement_unit = item['measurement_unit']
                mymodel.save()
