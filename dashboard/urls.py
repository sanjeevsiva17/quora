from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.question, name='question'),
    path('question/', views.add_question, name='add_question'),
    path('<int:question_id>/answer/', views.add_answer, name='add_answer'),
    path('<int:question_id>/edit/', views.edit_answer, name='edit_answer'),
    path('<int:question_id>/editq/', views.edit_question, name='edit_question'),
    path('<int:question_id>/delete_question/', views.delete_question, name='delete_question'),
    path('<int:answer_id>/delete_answer/', views.delete_answer, name='delete_answer'),
    path('<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('answer/upvote/', views.upvotes, name='upvotes'),
    path('profile/', views.user_profile, name='user_profile')

]
