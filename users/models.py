from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя.
    Добавляем дополнительные поля.
    """
    bio = models.TextField(
        verbose_name='О себе',
        max_length=500,
        blank=True,         # необязательное поле
        null=True,          # разрешаем NULL в базе
        help_text='Краткая информация о себе'
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/',
        blank=True,
        null=True
    )
    # Можно добавить и другие поля, например:
    # phone = models.CharField(max_length=15, blank=True, null=True)
    # city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username