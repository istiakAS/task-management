from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email']

    def clean_password1(self): # cleaning password field and checking if it meets the requirements
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append("Password must be at least 8 characters Long")

        if not re.search(r'[A-Z]', password1):
            errors.append("Password must include at least one uppercase letter")

        if not re.search(r'[a-z]', password1):
            errors.append("Password must include at least one lowercase letter")

        if not re.search(r'[0-9]', password1):
            errors.append("Password must include at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            errors.append("Password must include at least one special character")

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean(self):     #non field error  
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_email(self): # for cleaning email field and checking if email already exists in the database
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role",
    )

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permission = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permission"
    )
    class Meta:
        model = Group
        fields = ['name', 'permission']

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass 