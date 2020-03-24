from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.question, name='question'),
    path('question/',views.add_question, name='add_question'),
    path('answer/', views.add_answer, name='add_answer')

]
