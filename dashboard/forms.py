from django import forms
from .models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', ]
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 20, 'cols': 100}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', ]
        widgets = {
            'answer_text': forms.Textarea(attrs={'rows': 20, 'cols': 100}),
        }


# class QuestionEditForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text', ]
#         widgets = {
#             'question_text': forms.Textarea(attrs={'rows': 20, 'cols': 100}),
#         }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', ]
