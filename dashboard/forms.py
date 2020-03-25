from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields= ['question_text',]
        widgets = {
          'question_text': forms.Textarea(attrs={'rows':20, 'cols':100}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields=['answer_text',]
        widgets = {
          'answer_text': forms.Textarea(attrs={'rows':20, 'cols':100}),
        }
