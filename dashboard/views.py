from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from .models import Question, Answer, Comment, Vote
from .forms import QuestionForm, AnswerForm, CommentForm
from django.contrib import messages
import json


def index(request):
    questions = Question.objects.all()
    return render(request, "dashboard/dashboard.html", {"questions": questions})


def question(request, question_id):
    """
    Listing a particular question, answers, comments and votes

    The logged in user can add answer only once
    """
    question = get_object_or_404(Question, pk=question_id)
    final_answer = {}
    answer = Answer.objects.prefetch_related('comment_set').filter(question=question)

    for ans in answer:
        comments = ans.comment_set.all()
        final_answer[ans] = (comments, Vote.objects.filter(answer=ans).count())

    editable = False
    if request.user.is_authenticated:
        if Answer.already_answered(question_id=question.id, user_id=request.user.id):
            editable = True
        else:
            editable = False

    form = add_comment(request)

    return render(request, 'dashboard/question.html',
                  {"question": question, "editable": editable, "form": form, "final_answer": final_answer})


@login_required(login_url='/accounts/login/')
def add_comment(request):
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
    return form


@login_required(login_url='/accounts/login/')
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
        return render(request, 'dashboard/question_form.html', context)
    else:
        messages.info(request, "Login to add question")
        return redirect('login')


@login_required(login_url='/accounts/login/')
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
        return render(request, 'dashboard/answer_form.html', context)
    else:
        messages.info(request, "Login to answer")
        return redirect('login')


@login_required(login_url='/accounts/login/')
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
        return render(request, 'dashboard/edit_answer.html', context)
    else:
        messages.info(request, "Login to answer")
        return redirect('login')


@login_required(login_url='/accounts/login/')
def edit_question(request, question_id):
    if request.user.is_authenticated:
        ques = get_object_or_404(Question, pk=question_id)
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=ques)
            if form.is_valid():
                ans = form.save(commit=False)
                ans.user = request.user
                ans.question = ques
                ans.save()
                return redirect('index')
        else:
            form = QuestionForm(instance=ques)
        context = {'form': form, 'question': ques}
        return render(request, 'dashboard/edit_question.html', context)
    else:
        messages.info(request, "Login to answer")
        return redirect('login')



@login_required(login_url='/accounts/login/')
def delete_answer(request, answer_id):
    Answer.objects.filter(id=answer_id).delete()
    return redirect('user_profile')


@login_required(login_url='/accounts/login/')
def delete_question(request, question_id):
    Question.objects.filter(id=question_id).delete()
    return redirect('user_profile')


@login_required(login_url='/accounts/login/')
def delete_comment(request, comment_id):
    Comment.objects.filter(id=comment_id).delete()
    return redirect('user_profile')


@login_required(login_url='/accounts/login/')
def upvotes(request):
    if request.user.is_authenticated:
        user_id = request.POST.get("user")
        answer_id = request.POST.get("answer")

        vote_count = Vote.upvote_or_delete(answer_id, user_id)

        js = {"vote": vote_count, "answer":answer_id}
        return HttpResponse(json.dumps(js))
    else:
        messages.info(request, "Login to vote")
        return redirect('login')


@login_required(login_url='/accounts/login/')
def user_profile(request):
    user_data = request.user
    user_questions = Question.objects.filter(user_id=user_data.id)
    user_answers = Answer.objects.filter(user_id=user_data.id)
    user_comments = Comment.objects.filter(user_id=user_data.id)
    context = {"user_data": user_data, "user_questions": user_questions, "user_answers": user_answers,
               "user_comments": user_comments}
    return render(request, "dashboard/user_profile.html", context)
