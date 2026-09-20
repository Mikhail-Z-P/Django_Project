import json
import os

# Сначала настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# ТОЛЬКО ТЕПЕРЬ импортируем модели
from django.core import serializers
from catalog.models import Category, Product

def safe_export(model, filename):
    print(f"Выгружаем {model.__name__} в {filename}...")
    data_str = serializers.serialize('json', model.objects.all())
    data_obj = json.loads(data_str)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_obj, f, ensure_ascii=False, indent=4)
    print(f"Готово: {filename} (записано объектов: {len(data_obj)})")

os.makedirs('catalog/fixtures', exist_ok=True)

safe_export(Category, 'catalog/fixtures/categories.json')
safe_export(Product, 'catalog/fixtures/products.json')

print("Все данные успешно экспортированы!")
