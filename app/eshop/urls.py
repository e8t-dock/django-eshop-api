from django.urls import path, include 

from eshop import views

urlpatterns = [
  path('products/search/', views.search),

  path('products/', views.ProductsList.as_view()),
  path('products/<slug:category_slug>/<slug:product_slug>', views.ProductDetail.as_view()),
  path('products/<slug:category_slug>', views.CategoryDetail.as_view()),
  
]