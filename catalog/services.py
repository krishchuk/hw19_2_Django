from django.core.cache import cache

from catalog.models import Category, Product
from config.settings import CACHE_ENABLED


def get_categories_from_cache():
    """Получает список категорий из кэша, если он есть, или из БД"""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = "category_list"
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = Category.objects.all()
    cache.set(key, categories)
    return categories


def get_products_from_cache():
    """Получает список продуктов из кэша, если он есть, или из БД"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "home"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products