from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Reply, Review, ReviewLike


# Notify user when their review is approved or pinned
@receiver(pre_save, sender=Review)
def notify_review_status_change(sender, instance, **kwargs):
    if instance.pk:  # Ensure the review already exists before checking for changes
        previous = Review.objects.get(pk=instance.pk)

        if previous.status != instance.status:
            if instance.status == "approved":
                subject = "Your Review Has Been Approved!"
                message = f"Hi {instance.user.username},\n\nYour review has been approved and is now visible.\n\nThanks!"
            elif instance.status == "pinned":
                subject = "Your Review Has Been Pinned!"
                message = f"Hi {instance.user.username},\n\nYour review has been pinned as a featured review.\n\nThanks!"
            else:
                return  # No email needed for other status changes

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                fail_silently=True,
            )


# Notify user when their review gets a like
@receiver(post_save, sender=ReviewLike)
def notify_review_like(sender, instance, created, **kwargs):
    if created:
        review = instance.review
        subject = "Your Review Got a Like!"
        message = f"Hi {review.user.username},\n\nSomeone liked your review!\n\nThanks!"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [review.user.email],
            fail_silently=True,
        )


# Notify user when their review gets a reply
@receiver(post_save, sender=Reply)
def notify_review_reply(sender, instance, created, **kwargs):
    if created:
        review = instance.review
        subject = "Your Review Got a Reply!"
        message = f"Hi {review.user.username},\n\nYour review has received a reply from {instance.user.username}.\n\nThanks!"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [review.user.email],
            fail_silently=True,
        )
