from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (HomeListView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView,
                           ProductDeleteView, CategoryListView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),

    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),

    path('categories/', CategoryListView.as_view(), name='category_list'),
]
