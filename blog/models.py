from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'Новости'),
        ('technology', 'Технологии'),
        ('science', 'Наука'),
        ('art', 'Искусство'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='news',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100, verbose_name='Имя автора')
    
    def __str__(self):
        return f'Комментарий от {self.author_name} к статье "{self.article.title}"'