from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeListView, ContactsView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product'),
]
