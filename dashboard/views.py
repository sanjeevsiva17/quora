from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib import messages

def index(request):
    questions = Question.objects.all()
    return render(request, "dashboard.html", {"questions": questions})
    # return HttpResponse("Welcome to Quora 2.0")


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer.objects.filter(question=question)
    return render(request, 'question.html', {"question": question, "answers": answer})


def add_question(request):
    if request.user.is_authenticated:
        if request.method == "POST":
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
    else:
        messages.info(request, "Login to add question")
        return redirect('login')


def add_answer(request, question_id):
    if request.user.is_authenticated:
        ques = get_object_or_404(Question, pk=question_id)
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                ans = form.save(commit=False)
                ans.user = request.user
                ans.question = ques
                ans.save()
                return redirect('index')
        else:
            form = AnswerForm()
        context = {'form': form, 'question':ques}
        return render(request, 'answer_form.html', context)
    else:
        messages.info(request, "Login to answer")
        return redirect('login')


def votes(request):
    if request.user.is_authenticated:
        pass
    else:
        messages.info(request, "Login to vote")
        return redirect('login')
