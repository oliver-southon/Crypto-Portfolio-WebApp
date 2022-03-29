from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterTraderForm(UserCreationForm):
    class Meta:
        model = User

        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterTraderForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["password1"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["password2"].widget.attrs["class"] = "form-control form-control-sm"

