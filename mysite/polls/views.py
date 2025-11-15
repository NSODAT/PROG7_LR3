from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404

from .forms import QuestionForm, ChoiceForm, BulkChoiceForm

@login_required
def create_question_simple(request):
    """
    Простая форма создания опроса с текстовой областью для вариантов.
    Черновой вариант фронтенда.
    """
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        bulk_choice_form = BulkChoiceForm(request.POST)

        if question_form.is_valid() and bulk_choice_form.is_valid():
            # Сохраняем вопрос
            question = question_form.save(commit=False)
            question.author = request.user  # Сохраняем автора
            question.save()

            # Обрабатываем варианты ответов из текстовой области
            choices_text = bulk_choice_form.cleaned_data['choices_text']
            choices_list = [choice.strip() for choice in choices_text.split('\n') if choice.strip()]

            for choice_text in choices_list:
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    votes=0
                )

            return redirect('polls:detail', pk=question.id)
    else:
        question_form = QuestionForm()
        bulk_choice_form = BulkChoiceForm()

    return render(request, 'polls/create_question_simple.html', {
        'question_form': question_form,
        'bulk_choice_form': bulk_choice_form,
    })


@login_required
def create_question_advanced(request):
    """
    Продвинутая форма с динамическим добавлением полей для вариантов ответов.
    """
    ChoiceFormSet = formset_factory(ChoiceForm, extra=3, min_num=2, validate_min=True)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST, prefix='choices')

        if question_form.is_valid() and choice_formset.is_valid():
            # Сохраняем вопрос
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()

            # Сохраняем варианты ответов
            for form in choice_formset:
                if form.cleaned_data.get('choice_text'):
                    Choice.objects.create(
                        question=question,
                        choice_text=form.cleaned_data['choice_text'],
                        votes=0
                    )

            return redirect('polls:detail', pk=question.id)
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet(prefix='choices')

    return render(request, 'polls/create_question_advanced.html', {
        'question_form': question_form,
        'choice_formset': choice_formset,
    })


@login_required
def my_questions(request):
    """
    Список опросов, созданных текущим пользователем.
    """
    questions = Question.objects.filter(author=request.user).order_by('-pub_date')
    return render(request, 'polls/my_questions.html', {
        'questions': questions
    })

class IndexView(generic.ListView):
    """
    Дженерик-вью для отображения списка опросов.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Возвращает последние 5 опубликованных вопросов."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    """
    Дженерик-вью для отображения деталей опроса.
    """
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    """
    Дженерик-вью для отображения результатов опроса.
    """
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    """
    Обрабатывает голосование (остается функциональным вью).
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не выбрали вариант ответа.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
