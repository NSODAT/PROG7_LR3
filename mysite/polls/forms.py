from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    """
    Форма для создания нового опроса с динамическим добавлением вариантов ответов.
    """
    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': 'Текст вопроса',
        }
        widgets = {
            'question_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст вопроса'
            }),
        }

class ChoiceForm(forms.Form):
    """
    Форма для одного варианта ответа.
    """
    choice_text = forms.CharField(
        max_length=200,
        label='Вариант ответа',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вариант ответа'
        })
    )

class BulkChoiceForm(forms.Form):
    """
    Черновая форма для массового добавления вариантов ответов.
    """
    choices_text = forms.CharField(
        label='Варианты ответов',
        help_text='Введите каждый вариант ответа на отдельной строке',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Вариант 1\nВариант 2\nВариант 3'
        })
    )