import json
import os

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    extra_context = {
        'title': "Каталог"
    }


# def contacts(request):
#     context = {
#         'title': "Контакты"
#     }
#     # Получение данных от пользователя и их сохранение в JSON
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         user_contacts = {
#             'name': name,
#             'phone': phone,
#             'message': message
#         }
#         # Запись в уже существующий файл с данными
#         if os.path.isfile('data.json'):
#             with open('data.json', 'r') as file:
#                 user_data: list[dict] = json.load(file)
#                 user_data.append(user_contacts)
#             with open('data.json', 'w') as file:
#                 json.dump(user_data, file, indent=4)
#             # Вывод JSON в терминал
#             print(user_data)
#         # Создание файла и первая запись данных
#         else:
#             with open('data.json', 'w') as file:
#                 json.dump([user_contacts], file, indent=4)
#
#     return render(request, 'catalog/contacts.html', context)


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"
    extra_context = {
        'title': "Контакты"
    }

    def post(self, request):
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
                    json.dump([user_contacts], file, ensure_ascii=False, indent=4)

        return render(request, 'catalog/contacts.html')


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data()

        item = Product.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f"Товар: {item.name}"

        return context_data
