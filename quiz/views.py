from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
from random import randint
from registration.models import Register
import os

col_list = ["question_image", "correct_answer", "explanation"]

num_questions = 2


def get_questions(n):
    questions = pd.read_csv("quiz.csv", encoding='windows-1252', usecols=col_list)["question_image"]
    answers = pd.read_csv("quiz.csv", encoding='windows-1252', usecols=col_list)["correct_answer"]
    explanation = pd.read_csv("quiz.csv", encoding='windows-1252', usecols=col_list)["explanation"]
    question_list = []
    for i in range(n):
        rand_ques_num = randint(0, n)
        question_list.append([list(questions)[rand_ques_num], list(answers)[rand_ques_num], list(explanation)[rand_ques_num]])
    # list_of_questions = zip(list(questions), list(answers), list(explanation))
    # return render(request, "index.html", {'ques': list_of_questions})
    return question_list


def start(request):
    if request.method == "POST" and request.user.is_authenticated:
        username = request.user.get_full_name()
        request.session['questions'] = get_questions(num_questions)
        request.session['qno'] = 0
        request.session['score'] = 0
        return render(request, 'instructions.html', {'user': username})


def test_start(request):
    if request.method == "POST" and request.user.is_authenticated:
        username = request.user.get_full_name()
        qno = int(request.session['qno'])
        q = list(request.session['questions'])
        s = int(request.session['score'])
        return render(request, 'quiz.html', {'user': username, 'ques': q[qno][0], 'num': qno+1, 'score': s})


def next_ques(request):
    if request.method == "POST" and request.user.is_authenticated:
        username = request.user.get_full_name()
        ans = request.POST['answer']
        qno = int(request.session['qno'])
        q = list(request.session['questions'])
        s = int(request.session['score'])
        if ans == q[qno][1]:
            request.session['score'] = s = s + 1
        global num_questions
        request.session['qno'] = qno = qno + 1
        if qno < num_questions:
            return render(request, 'quiz.html', {'user': username, 'ques': q[qno][0], 'num': qno+1, 'score': s})
        else:
            return render(request, 'complete.html', {'user': username, 'score': s})


def submit(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            name = request.user.get_full_name()
            usn = request.user.get_username()
            email = request.user.get_email_field_name()
            Register.objects.create(name=name, usn=usn, email=email, score1=int(request.session['score']))
            return render(request, 'thanks.html')
        except Exception as e:
            return render(request, 'responded.html', {"user": request.user.get_full_name()})