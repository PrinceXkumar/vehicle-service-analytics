from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Service
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "full_name", "phone", "address", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set Bootstrap classes and placeholders
        field_placeholders = {
            "username": "e.g. johndoe",
            "email": "you@example.com",
            "password1": "Create a strong password",
            "password2": "Re-enter your password",
            "full_name": "John Doe",
            "phone": "+1 555 123 4567",
            "address": "Street, City, ZIP",
        }

        for field_name, field in self.fields.items():
            if field_name == "role":
                field.widget.attrs.setdefault("class", "form-select")
                continue

            # Textarea rows for address
            if field_name == "address":
                field.widget.attrs.setdefault("rows", "3")

            # Default form-control for others
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()

            if field_name in field_placeholders:
                field.widget.attrs.setdefault("placeholder", field_placeholders[field_name])


class BookServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["service_type"]
        widgets = {
            "service_type": forms.Select(attrs={"class": "form-select"}),
        }


class AssignMechanicForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["assigned_mechanic"]
        widgets = {
            "assigned_mechanic": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_mechanic"].queryset = User.objects.filter(profile__role=Profile.ROLE_MECHANIC)


class UpdateServiceStatusForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
        }