from django.contrib import admin

from .models import Reply, Review, ReviewLike


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "wellness_place", "rating", "status", "created_at")
    list_filter = ("status", "rating", "created_at")
    search_fields = ("user__username", "wellness_place__name", "comment")
    list_editable = ("status",)  # Allow changing status directly
    ordering = ("-created_at",)
    readonly_fields = ("user",)  # Prevents editing the user field

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the user when creating a new review
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "review", "created_at")
    search_fields = ("user__username", "review__comment")
    readonly_fields = ("user",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "review", "created_at")
    search_fields = ("user__username", "review__comment", "text")
    ordering = ("-created_at",)
    readonly_fields = ("user",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)
