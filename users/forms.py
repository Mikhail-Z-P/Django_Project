from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'country', 'avatar',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(
                request=None,
                username=email,
                password=password,
            )
            if user is None:
                raise forms.ValidationError(
                    'Неверный email или пароль.'
                )
            cleaned_data['user'] = user
        return cleaned_data