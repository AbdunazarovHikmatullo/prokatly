from django import forms
from .models import User

# Переименуем класс для ясности, если это форма регистрации
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        }
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Такой пользователь уже существует")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# Форма входа
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control", # Класс для поля ввода
            "placeholder": "Ваше имя"
        })
    )
    password = forms.CharField(
        label="Ваш пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control", # Класс для поля ввода
            "placeholder": "Пароль"
        })
    )