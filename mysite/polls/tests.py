import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days):
    """
    Создает вопрос с заданным текстом и смещением дней от текущего времени.
    Положительные дни - в будущем, отрицательные - в прошлом.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """
    Тесты для модели Question.
    """

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() возвращает False для вопросов с pub_date в будущем.
        """
        future_question = create_question("Будущий вопрос", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() возвращает False для вопросов старше 1 дня.
        """
        old_question = create_question("Старый вопрос", days=-30)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() возвращает True для вопросов за последние сутки.
        """
        recent_question = create_question("Недавний вопрос", days=-1)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    """
    Тесты для представления списка вопросов.
    """

    def test_no_questions(self):
        """
        Если вопросов нет, отображается соответствующее сообщение.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных опросов.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Вопросы с датой публикации в прошлом отображаются на странице индекса.
        """
        question = create_question("Прошлый вопрос", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Вопросы с датой публикации в будущем не отображаются на странице индекса.
        """
        create_question("Будущий вопрос", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Нет доступных опросов.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Даже если существуют и прошлые и будущие вопросы, отображаются только прошлые.
        """
        past_question = create_question("Прошлый вопрос", days=-30)
        create_question("Будущий вопрос", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question],
        )

    def test_two_past_questions(self):
        """
        На странице индекса может отображаться несколько вопросов.
        """
        question1 = create_question("Прошлый вопрос 1", days=-30)
        question2 = create_question("Прошлый вопрос 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """
    Тесты для представления деталей вопроса.
    """

    def test_future_question(self):
        """
        Детальное представление вопроса с pub_date в будущем возвращает 404.
        """
        future_question = create_question("Будущий вопрос", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Детальное представление вопроса с pub_date в прошлом отображает текст вопроса.
        """
        past_question = create_question("Прошлый вопрос", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
