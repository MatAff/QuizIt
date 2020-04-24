
from django.urls import path

from . import views

app_name = 'quizit'

urlpatterns = [
    path('', views.home, name='quizit-home'),
    path('go/', views.go, name='quizit-go'),
    path('home/', views.home, name='quizit-home'),
    path('about/', views.about, name='quizit-about'),
    path('basic/', views.basic, name='quizit-basic'),
    path('<int:item_id>/answer/', views.answer, name='answer'),
]
