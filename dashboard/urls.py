from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.question, name='question'),
    path('question/', views.add_question, name='add_question'),
    path('<int:question_id>/answer/', views.add_answer, name='add_answer'),
    path('<int:question_id>/edit/', views.edit_answer, name='edit_answer'),
    path('<int:question_id>/delete_question/', views.delete_question, name='delete_question'),
    path('<int:answer>/delete_answer/', views.delete_answer, name='delete_answer'),
    path('answer/upvote/', views.upvotes, name='upvotes')
]
