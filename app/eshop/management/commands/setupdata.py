import random

from django.db import transaction
from django.core.management.base import BaseCommand

from eshop.models import Category, Product
from eshop.factories import (
  CategoryFactory,
  ProductFactory
)

NUM_CATEGORY=5
NUM_PRODUCT=50
PRODUCT_PER_CATEGORY=10

class Command(BaseCommand):
  help = "Generates dummy data"

  @transaction.atomic
  def handle(self, *args, **kwargs):
    self.stdout.write("Deleteing old data")
    models = [Category, Product]
    for m in models:
      # m.objects.all().delete()
      m.truncate()

    self.stdout.write("Creating new data")
    categories = []
    for _ in range(NUM_CATEGORY):
      category = CategoryFactory()
      categories.append(category)
      # for _ in range (PRODUCT_PER_CATEGORY):
      #   ProductFactory(category=category)

    for _ in range(NUM_PRODUCT):
      category = random.choice(categories)
      ProductFactory(category=category)

