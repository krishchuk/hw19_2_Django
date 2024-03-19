import json
import os

from django.shortcuts import render

from catalog.models import Category, Product


def home(request):
    products_list = Product.objects.all()
    for prod in products_list:
        prod.description = prod.description[0:100]
    context = {
        'products_list': products_list,
        'title': "Каталог"
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    context = {
        'title': "Контакты"
    }
    # Получение данных от пользователя и их сохранение в JSON
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user_contacts = {
            'name': name,
            'phone': phone,
            'message': message
        }
        # Запись в уже существующий файл с данными
        if os.path.isfile('data.json'):
            with open('data.json', 'r') as file:
                user_data: list[dict] = json.load(file)
                user_data.append(user_contacts)
            with open('data.json', 'w') as file:
                json.dump(user_data, file, indent=4)
            # Вывод JSON в терминал
            print(user_data)
        # Создание файла и первая запись данных
        else:
            with open('data.json', 'w') as file:
                json.dump([user_contacts], file, indent=4)

    return render(request, 'catalog/contacts.html', context)


def product(request, pk):
    item = Product.objects.get(pk=pk)
    context = {
        'products_list': Product.objects.filter(id=pk),
        'title': f"Товар: {item.name}"
    }
    return render(request, 'catalog/product.html', context)
