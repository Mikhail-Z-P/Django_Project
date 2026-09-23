from django.core.cache import cache
from .models import Product


def get_product_by_pk(pk):
    """Возвращает продукт по pk с кешированием в Redis."""
    cache_key = f"product_{pk}"
    product = cache.get(cache_key)
    if product is None:
        product = Product.objects.get(pk=pk)
        cache.set(cache_key, product, 300)
    return product


def invalidate_product_cache(pk):
    """Сбрасывает кеш продукта и общего списка продуктов."""
    cache.delete(f"product_{pk}")
    cache.delete("products_list")


def get_products_by_category(category_id):
    """Возвращает список опубликованных продуктов в категории с кешированием."""
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)
    if products is None:
        products = list(
            Product.objects.filter(category_id=category_id, is_published=True)
        )
        cache.set(cache_key, products, 300)
    return products


def get_published_products():
    """Возвращает список опубликованных продуктов с кешированием."""
    cache_key = "products_list"
    products = cache.get(cache_key)
    if products is None:
        products = list(Product.objects.filter(is_published=True))
        cache.set(cache_key, products, 300)
    return products
