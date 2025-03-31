from django import forms

from .models import Reply, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["wellness_place", "rating", "comment"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["review", "text"]
