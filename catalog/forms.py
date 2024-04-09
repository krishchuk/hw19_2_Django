from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version

wrong_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForms(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'picture', 'category', 'price',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for word in wrong_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Недопустимое название продукта')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in wrong_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Недопустимое описание продукта')
        return cleaned_data


class VersionForms(StyleFormMixin, forms.ModelForm):
    # active_versions = []

    class Meta:
        model = Version
        fields = "__all__"

    # def get_context(self):
    #     context = super().get_context()
    #
    #     if Version.is_active is True:
    #         self.active_versions.append(1)
    #     if len(self.active_versions) > 1:
    #         raise forms.ValidationError("Может быть только одна активная версия!")
    #
    #     # product = Product
    #     # active_versions: list = product.filter(is_active=True)
    #     # if len(active_versions) > 1:
    #     #     raise ValueError("Может быть только одна активная версия!")
    #
    #     return context
