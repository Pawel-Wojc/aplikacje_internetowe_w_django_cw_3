from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxLengthValidator

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

User = get_user_model()
class UserSettingsForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Nazwa użytkownika',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        max_length=100,
        required=False,
        label='Opis',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'maxlength': 100,
            'placeholder': 'Napisz coś o sobie...'
        })
    )
    avatar = forms.ImageField(
        required=False,
        label='Avatar',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username',  'avatar', 'bio']

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        exists = User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists()
        if exists:
            raise forms.ValidationError('Taka nazwa użytkownika już istnieje.')
        return username


    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '').strip()
        if len(bio) > 100:
            raise forms.ValidationError('Opis może mieć maksymalnie 100 znaków.')
        return bio

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            valid_types = ['image/jpeg', 'image/png']
            if hasattr(avatar, 'content_type') and avatar.content_type not in valid_types:
                raise forms.ValidationError('Dozwolone są tylko pliki JPG i PNG.')
        return avatar


class CustomUserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Obecne hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'})
    )
    new_password1 = forms.CharField(
        label='Nowe hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )
    new_password2 = forms.CharField(
        label='Powtórz nowe hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )