from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for submitting a product rating and optional comment."""

    class Meta:
        model = Comment
        fields = ["rating", "text", "guest_name", "guest_email"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "text": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        """Require guest name and email when no user is set in ``initial``.

        Returns:
            dict: The cleaned form data.
        """
        data = super().clean()
        user = self.initial.get("user")
        if not user and not data.get("guest_name"):
            self.add_error("guest_name", "Required for guest.")
        if not user and not data.get("guest_email"):
            self.add_error("guest_email", "Required for guest.")
        return data
