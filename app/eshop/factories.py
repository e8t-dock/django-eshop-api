import factory
from factory.django import DjangoModelFactory

from .models import Category, Product

from faker import Faker
from faker.providers import DynamicProvider

categories_provider = DynamicProvider(
  provider_name="category",
  elements=['Home & Kitchen', 'Beauty & Personal Car', 'Clothing, Shoes & Jewelry', 'Toys & games', 'Health, Household & Baby Care', 'Baby', 'Electronics', 'Sports & outdoors', 'Pet Supplies', 'Office Supplies'],
)

fake = Faker()

# then add new provider to faker instance
fake.add_provider(categories_provider)

# now you can use:
# fake.medical_profession()
# 'dr.'

class CategoryFactory(DjangoModelFactory):
  class Meta:
    model = Category
  name = fake.unique.category()

class ProductFactory(DjangoModelFactory):
  class Meta:
    model = Product
  category = factory.SubFactory(CategoryFactory)
  name = factory.Faker("first_name")
  # name = fake.first_name()
  description = fake.sentence(nb_words=50)
  price = fake.random_number(digits=3)
  image = factory.django.ImageField(color='blue')
  thumbnail = factory.django.ImageField(color='blue')