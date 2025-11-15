from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # Новые URLs для создания опросов
    path('create/simple/', views.create_question_simple, name='create_simple'),
    path('create/advanced/', views.create_question_advanced, name='create_advanced'),
    path('my-questions/', views.my_questions, name='my_questions'),
]