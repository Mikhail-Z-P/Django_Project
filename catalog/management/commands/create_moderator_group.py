from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Создаёт группу модераторов продуктов"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Право отмены публикации
        can_unpublish = Permission.objects.get(
            codename="can_unpublish_product",
            content_type__app_label="catalog",
        )

        # Право удаления любого продукта
        can_delete = Permission.objects.get(
            codename="delete_product",
            content_type__app_label="catalog",
        )

        group.permissions.add(can_unpublish, can_delete)
        self.stdout.write(
            self.style.SUCCESS(
                f'Группа "Модератор продуктов" {"создана" if created else "обновлена"}'
            )
        )
