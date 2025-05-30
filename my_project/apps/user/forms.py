from django import forms
from .models import CustomUser
# from django.contrib.auth.models import User
# from django.contrib.auth.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import serializers
import re
from django.core.exceptions import ValidationError
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    #  Configuration
    class Meta():
        model = CustomUser
        # fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'contact']
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'contact', 'dob']
        widgets = {
            # 'dob': forms.extras.SelectDateWidget
            'dob': forms.SelectDateWidget(years=range(1980, 2015))
        }


class UserCreationForm(serializers.Serializer):
    # username = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    is_staff = serializers.BooleanField(required=False, default=False)



# def validate_password(value):
#     # if re.search()
#     breakpoint()
#     if not bool(re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value)):
#         raise ValidationError("Password must contain Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.")
#     return value

class ResetPassword(forms.Form):
    password = forms.CharField(max_length=30)
    # password = forms.CharField(max_length=30, validators=[validate_password])

    def clean_password(self):
        # if re.search()
        # breakpoint()
        if not bool(re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", self.cleaned_data['password'])):
            raise ValidationError("Password must contain Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.")
        return self.cleaned_data['password']