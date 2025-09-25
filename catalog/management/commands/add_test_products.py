from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import random


class Command(BaseCommand):
    help = 'Reset database and add test products'

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()


        category1 = Category.objects.create(name="Bryophyta")
        category2 = Category.objects.create(name="Conifers")
        category3 = Category.objects.create(name="Polypodiopsida")
        category4 = Category.objects.create(name="Rhodophyta")


        for i in range(10):
            Product.objects.create(
                name=f"Product {i + 1}",
                price=round(random.uniform(10.0, 100.0), 2),
                category=random.choice([category1, category2,category3,category4])
            )

        self.stdout.write("Database reset complete!")


