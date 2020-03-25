from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Question, Answer, Comment, Vote
from .forms import QuestionForm, AnswerForm, CommentForm
from django.contrib import messages


def index(request):
    questions = Question.objects.all()
    return render(request, "dashboard.html", {"questions": questions})


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    final_answer = {}
    answer = Answer.objects.filter(question=question)
    for ans in answer:
        comments = Comment.objects.filter(answer=ans)
        final_answer[ans] = (comments, Vote.objects.filter(answer=ans).count())
    editable = False
    form = CommentForm()
    if request.user.is_authenticated:
        if Answer.objects.filter(question_id=question_id, user=request.user).exists():
            editable = True
        else:
            editable = False

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                ans = get_object_or_404(Answer, pk=form.data["answer_id"])
                post.answer = ans
                post.save()
        else:
            form = CommentForm()
    return render(request, 'question.html',
                  {"question": question, "editable": editable, "form": form, "final_answer": final_answer})


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
        context = {'form': form, 'question': ques}
        return render(request, 'answer_form.html', context)
    else:
        messages.info(request, "Login to answer")
        return redirect('login')


def edit_answer(request, question_id):
    if request.user.is_authenticated:
        ques = get_object_or_404(Question, pk=question_id)
        instance = Answer.objects.filter(question_id=question_id, user=request.user).first()
        if request.method == "POST":
            form = AnswerForm(request.POST, instance=instance)
            if form.is_valid():
                ans = form.save(commit=False)
                ans.user = request.user
                ans.question = ques
                ans.save()
                return redirect('index')
        else:
            form = AnswerForm(instance=instance)
        context = {'form': form, 'question': ques}
        return render(request, 'edit_answer.html', context)
    else:
        messages.info(request, "Login to answer")
        return redirect('login')


def delete_answer(request, answer_id):
    Answer.objects.filter(id=answer_id).delete()


def delete_question(request, question_id):
    Question.objects.filter(id=question_id).delete()


def upvotes(request):
    if request.user.is_authenticated:
        user_id =  request.POST.get("user")
        answer_id = request.POST.get("answer")
        vote = Vote.objects.filter(answer_id=answer_id, user_id=user_id)
        if vote.exists():
            vote.delete()
            return HttpResponse("deleted")
        else:
            Vote.objects.create(answer_id=answer_id, user_id=user_id)
            return HttpResponse("created")
    else:
        messages.info(request, "Login to vote")
        return redirect('login')
