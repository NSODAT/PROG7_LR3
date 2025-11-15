from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """
    Inline-отображение для вариантов ответа в админке вопросов.
    """
    model = Choice
    extra = 3  # Количество дополнительных пустых полей для вариантов


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Кастомизированный административный интерфейс для модели Question.
    """
    # Поля для отображения в списке вопросов
    list_display = ['question_text', 'pub_date', 'was_published_recently']

    # Фильтры по дате публикации
    list_filter = ['pub_date']

    # Поиск по тексту вопроса
    search_fields = ['question_text']

    # Разбивка полей на группы в форме редактирования
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Информация о дате', {
            'fields': ['pub_date'],
            'classes': ['collapse'],
            'description': 'Дата и время публикации вопроса'
        }),
    ]

    # Inline-отображение вариантов ответа
    inlines = [ChoiceInline]

    # Дата-пикер для поля pub_date
    date_hierarchy = 'pub_date'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """
    Кастомизированный административный интерфейс для модели Choice.
    """
    list_display = ['choice_text', 'question', 'votes']
    list_filter = ['question']
    search_fields = ['choice_text', 'question__question_text']


# Кастомизация заголовка админки
admin.site.site_header = "Панель администратора системы опросов"
admin.site.site_title = "Система опросов"
admin.site.index_title = "Управление опросами"