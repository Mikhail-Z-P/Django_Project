from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(verbose_name="описание")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="изображение"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="категория"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="дата последнего изменения"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    class Meta:
        permissions = [
            ("can_unpublish_product", "Может отменить публикацию продукта"),
        ]
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    def __str__(self):
        return self.name
