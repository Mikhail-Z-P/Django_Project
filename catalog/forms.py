from django import forms
from django.conf import settings
from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                # Чекбокс: стилизуем как переключатель
                field.widget.attrs['class'] = 'form-check-input'
                field.widget.attrs['style'] = 'margin-left: 10px;'
            else:
                # Все остальные поля: текстовый ввод, textarea и т.д.
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "category"]

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        name_lower = name.lower()
        for word in settings.FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    f'Слово «{word}» запрещено к использованию в названии.'
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        description_lower = description.lower()
        for word in settings.FORBIDDEN_WORDS:
            if word in description_lower:
                raise forms.ValidationError(
                    f'Слово «{word}» запрещено к использованию в описании.'
                )
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError(
                'Цена не может быть отрицательной.'
            )
        return price
