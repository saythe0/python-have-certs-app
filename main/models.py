from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$',
        message="Телефон должен быть в формате: 8(XXX)XXX-XX-XX"
    )
    
    fio = models.CharField(
        max_length=255, 
        verbose_name='ФИО',
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ\s]+$',
                message='ФИО должно содержать только буквы кириллицы и пробелы'
            )
        ]
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        unique=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Завершено обучение'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('phone', 'Переводом по номеру телефона'),
    ]
    
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name='Пользователь'
    )
    course_name = models.CharField(
        max_length=255, 
        verbose_name='Название курса'
    )
    start_date = models.DateField(
        verbose_name='Дата начала'
    )
    payment_method = models.CharField(
        max_length=10, 
        choices=PAYMENT_CHOICES,
        verbose_name='Способ оплаты'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course_name} - {self.user.username}"


class Review(models.Model):
    application = models.OneToOneField(
        Application, 
        on_delete=models.CASCADE, 
        related_name='review',
        verbose_name='Заявка'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв на {self.application.course_name}"