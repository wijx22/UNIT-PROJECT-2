from django.contrib import admin

from .models import Booking, UserProfile, WellnessPlace, WellnessService, WhatToExpect


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


@admin.register(WellnessPlace)
class WellnessPlaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "language",
        "experience_type",
        "health_condition",
    )
    list_filter = ("location", "language", "experience_type", "health_condition")
    search_fields = ("name", "description")


class WhatToExpectInline(admin.TabularInline):
    model = WhatToExpect
    extra = 1  # Number of empty forms shown


@admin.register(WellnessService)
class WellnessServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "place", "short_description")
    list_filter = ("place",)
    search_fields = ("title", "description", "place__name")
    inlines = [WhatToExpectInline]

    def short_description(self, obj):
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )

    short_description.short_description = "Description"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "session_type", "booking_date")
    list_filter = ("session_type", "booking_date")
    search_fields = ("user__username", "user__email", "service__title")
