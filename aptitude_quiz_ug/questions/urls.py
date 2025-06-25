from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('new/', views.question_create, name='question_create'),
    path('start/<str:category>/', views.start_quiz, name='start_quiz'),
    path('take/', views.take_quiz, name='take_quiz'),
    path('result/', views.quiz_result, name='quiz_result'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),

]
