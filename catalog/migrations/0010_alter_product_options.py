# Generated by Django 4.2 on 2024-04-21 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'permissions': [('set_published_status', 'Can publish product')], 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
    ]