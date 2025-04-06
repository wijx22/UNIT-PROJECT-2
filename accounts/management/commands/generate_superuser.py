from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "command for creating superuser"

    def handle(self, *args, **options):
        try:
            user = User.objects.create(
                username="admin",
                password="1111",
                email="admin@admin.com",
                first_name="admin",
                last_name="admin",
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )
        except:
            user = User.objects.get(is_superuser=True)
        user.set_password("1111")
        user.save()
