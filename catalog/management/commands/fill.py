import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """Получаем данные из фикстурв с категориями"""
        with open('fixture_category_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_products():
        """Получаем данные из фикстурв с продуктами"""
        with open('fixture_product_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def handle(self, *args, **options):
        """Очищаем таблицы и заполняем их заново"""
        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(pk=category.get('pk'), **category["fields"])
            )

        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(category=Category.objects.get(pk=product['fields']["category"]),
                        name=product['fields']["name"],
                        pk=product['pk'],
                        description=product['fields']["description"],
                        picture=product['fields']["picture"],
                        price=product['fields']["price"],
                        created_at=product['fields']["created_at"],
                        updated_at=product['fields']["updated_at"],)
            )

        Product.objects.bulk_create(product_for_create)
