from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from services import  get_product_by_pk, invalidate_product_cache
from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    """Отображает список всех опубликованных продуктов на главной странице.
    Модераторы видят все продукты, включая неопубликованные.
    Обычные пользователи и гости — только опубликованные.
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Возвращает queryset с фильтрацией по статусу публикации."""
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.has_perm("catalog.can_unpublish_product"):
            return queryset
        return queryset.filter(is_published=True)


class ContactsView(TemplateView):
    """Отображает страницу с контактной информацией."""

    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    """Отображает детальную информацию о конкретном продукте."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        """Возвращает продукт через сервис с кешированием по pk."""
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_product_by_pk(pk)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """Привязывает текущего пользователя как владельца продукта
        перед сохранением формы.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        """Проверяет, что текущий пользователь — владелец продукта
        или модератор. Возвращает True, если доступ разрешён.
        """
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm("catalog.can_unpublish_product")

    def form_valid(self, form):
        """Сохраняет продукт и сбрасывает его кеш."""
        response = super().form_valid(form)
        invalidate_product_cache(self.object.pk)
        return response



class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        """Проверяет, что текущий пользователь — владелец продукта
        или модератор с правом удаления. Возвращает True, если доступ разрешён.
        """
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm("catalog.delete_product")

    def form_valid(self, form):
        """Удаляет продукт и сбрасывает его кеш."""
        pk = self.object.pk
        response = super().form_valid(form)
        invalidate_product_cache(pk)
        return response



class ProductUnpublishView(PermissionRequiredMixin, View):
    """Снятие продукта с публикации."""

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        """Снимает продукт с публикации: находит продукт по pk,
        устанавливает is_published=False и перенаправляет на главную.
        """
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        invalidate_product_cache(pk)
        return redirect("catalog:home")
