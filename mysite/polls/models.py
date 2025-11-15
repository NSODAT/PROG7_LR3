import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    pub_date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Опубликован недавно?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_total_votes(self):
        """Возвращает общее количество голосов для этого вопроса"""
        return sum(choice.votes for choice in self.choice_set.all())


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    choice_text = models.CharField(max_length=200, verbose_name="Текст варианта")
    votes = models.IntegerField(default=0, verbose_name="Количество голосов")

    def __str__(self):
        return self.choice_text
