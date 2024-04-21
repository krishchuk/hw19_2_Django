import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from catalog.models import Product, Version
from catalog.forms import ProductForms, VersionForms, ProductModeratorForms


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    extra_context = {
        'title': "Каталог"
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for product in context_data['object_list']:
            active_version = product.version_set.filter(is_active=True).last()
            product.active_version = active_version
        return context_data


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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data()
        item = Product.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f"Товар: {item.name}"
        product = self.object
        active_version = product.version_set.filter(is_active=True).last()
        product.active_version = active_version
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForms
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': "Добавить продукт"
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForms, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.name)
            new_post.owner = self.request.user
            new_post.save()
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForms
    # permission_required = "catalog.change_product"
    extra_context = {
        'title': "Изменить продукт"
    }

    def get_form_class(self):
        user = self.request.user
        # if user == self.object.owner:
        if user == self.object.owner:
            return ProductForms
        if user.has_perm('catalog.set_published_status'):
            return ProductModeratorForms
        raise PermissionDenied

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForms, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': "Удалить продукт"
    }
