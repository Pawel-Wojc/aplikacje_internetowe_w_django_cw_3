from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'avatar', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Login'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Hasło'
    }))