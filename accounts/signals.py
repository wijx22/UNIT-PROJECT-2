from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import UserProfile

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def handle_user_creation(sender, instance: CustomUser, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        # If role is Admin, make them staff
        if instance.role == CustomUser.Role.ADMIN:
            instance.is_staff = True

            # Assign permissions to the Admin
            permissions = Permission.objects.filter(
                content_type__model__in=[
                    "review",
                    "reviewlike",
                    "reply",
                    "wellnessplace",
                    "wellnessservice",
                    "whattoexpect",
                    "booking",
                ]
            )
            instance.user_permissions.set(permissions)

            instance.save()
        elif instance.is_superuser:
            instance.role = CustomUser.Role.ADMIN
            instance.save()
