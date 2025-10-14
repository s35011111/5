from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Reset database and load categories and products'

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()


        call_command('loaddata', 'categories.json')
        call_command('loaddata', 'products.json')

        self.stdout.write("Database reset complete!")