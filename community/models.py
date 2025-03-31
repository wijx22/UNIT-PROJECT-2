from django.conf import settings
from django.db import models


class Review(models.Model):
    wellness_place = models.ForeignKey(
        "base.WellnessPlace", on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} Stars") for i in range(1, 6)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("approved", "approved"),
        ("unapproved", "unapproved"),
        ("pinned", "pinned"),
    ]
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="unapproved"
    )

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} Stars"

    def likes_count(self):
        return self.likes.all().count()


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username}"
