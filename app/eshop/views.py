from django.shortcuts import render
from django.http import Http404
from django.db.models import Q 

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.decorators import api_view 

# Create your views here.

from .models import Product, Category
from .serializers import ProductSerializer

class ProductsList(APIView):
  def get(self, request, format=None):
    products = Product.objects.all()[0:4]
    serializers = ProductSerializer(products, many=True)
    return Response(serializers.data)

class ProductDetail(APIView):
  def get_object(self, category_slug, product_slug):
    try:
      # return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
      return Product.objects.filter(category__slug=category_slug).filter(slug=product_slug)[0]
    except Product.DoesNotExist:
      raise Http404

  def get(self, request, category_slug, product_slug, format=None):
    product = self.get_object(category_slug, product_slug)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

class CategoryDetail(APIView):
  def get_object(self, category_slug):
    try:
      return Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
      raise Http404

  def get(self, request, category_slug,  format=None):
    category = self.get_object(category_slug)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

# search api 

@api_view(['POST'])
def search(request):
  query = request.data.get('q', '')
  if query:
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
  else:
    return Response({'products':[]})