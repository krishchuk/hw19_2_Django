# Generated by Django 5.0.2 on 2024-03-23 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_news_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='news/', verbose_name='изображение'),
        ),
    ]
