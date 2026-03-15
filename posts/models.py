from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    text = models.TextField('Текст поста', max_length=1000)
    image = models.ImageField('Изображение', upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # новые посты первыми
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'Пост {self.author} от {self.created_at:%d.%m.%Y}'