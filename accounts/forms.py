from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User

class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        label=_('Email'),
        help_text=_('Введите ваш действующий адрес электронной почты')
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """Форма обновления основной информации пользователя"""
    email = forms.EmailField(
        label=_('Email'),
        help_text=_('Введите ваш действующий адрес электронной почты')
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    """Форма обновления дополнительной информации профиля"""
    birth_date = forms.DateField(
        label=_('Дата рождения'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text=_('Формат: ДД.ММ.ГГГГ')
    )
    
    class Meta:
        model = User
        fields = ['avatar', 'bio', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'avatar': _('Загрузите ваше фото или аватар'),
            'bio': _('Расскажите немного о себе'),
        } 