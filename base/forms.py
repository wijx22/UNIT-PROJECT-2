from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "full_name",
            "phone_number",
            "session_type",
            "preferred_date",
            "preferred_time",
            "additional_notes",
        ]
