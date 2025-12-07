from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import CustomUser, Application, Review
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        min_length=6,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]+$',
                message='Логин может содержать только латинские буквы и цифры'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин (минимум 6 символов)'
        })
    )
    
    password1 = forms.CharField(
        label='Пароль',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль (минимум 8 символов)'
        })
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    
    fio = forms.CharField(
        label='ФИО',
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ\s]+$',
                message='ФИО должно содержать только буквы кириллицы и пробелы'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ФИО'
        })
    )
    
    phone = forms.CharField(
        label='Телефон',
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате: 8(XXX)XXX-XX-XX'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '8(XXX)XXX-XX-XX'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms. EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'fio', 'phone', 'email')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser. objects.filter(email=email). exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже существует')
        return phone


class CustomAuthenticationForm(AuthenticationForm):
    username = forms. CharField(
        label='Логин',
        widget=forms. TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин'
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    
    error_messages = {
        'invalid_login': 'Неверный логин или пароль',
        'inactive': 'Этот аккаунт неактивен',
    }
    
class ApplicationForm(forms.ModelForm):
    course_name = forms.CharField(
        label='Название курса',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название курса'
        })
    )
    
    start_date = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today(). strftime('%Y-%m-%d')
        }),
        input_formats=['%Y-%m-%d']
    )
    
    payment_method = forms. ChoiceField(
        label='Способ оплаты',
        choices=Application.PAYMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Application
        fields = ['course_name', 'start_date', 'payment_method']
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError('Дата начала не может быть раньше сегодняшней даты')
        return start_date


class ReviewForm(forms.ModelForm):
    text = forms.CharField(
        label='Ваш отзыв',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Напишите ваш отзыв о курсе...',
            'rows': 5
        })
    )
    
    class Meta:
        model = Review
        fields = ['text']