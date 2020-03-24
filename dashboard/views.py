from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Question, Answer
from .forms import  QuestionForm, AnswerForm

def index(request):
    questions = Question.objects.all()
    return render(request, "dashboard.html", {"questions": questions})
    # return HttpResponse("Welcome to Quora 2.0")


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer.objects.filter(question=question)
    return render(request, 'question.html', {"question": question, "answers": answer})

def add_question(request):
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'question_form.html', context)