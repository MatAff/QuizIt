from django.urls import path

from . import views

app_name = 'quizit'

urlpatterns = [
    path('', views.basic, name='quizit-basic'),
    path('about/', views.about, name='quizit-about'),
    path('basic/', views.basic, name='quizit-basic'),  
    path('<int:item_id>/basic/', views.basic, name='basic'),
    path('flagged/', views.flagged, name='quizit-flagged'),  
    path('update-content/', views.update_content, name='update-content'),  
    path('remove-flagged/', views.remove_flagged, name='remove-flagged'),  
]
