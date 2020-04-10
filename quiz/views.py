from django.template import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
from random import randint
from registration.models import Register
from django.contrib.auth import logout
from datetime import datetime, timedelta
from quiz import settings

col_list = ["question_image", "correct_answer", "explanation"]

num_questions = settings.NUM_OF_QUESTIONS
quiz_time = settings.SESSION_COOKIE_AGE
test_name = settings.TEST_NAME


def get_questions(n):
    try:
        questions = pd.read_csv("quiz.csv", encoding='windows-1252', usecols=col_list)["question_image"]
        answers = pd.read_csv("quiz.csv", encoding='windows-1252', usecols=col_list)["correct_answer"]
        explanation = pd.read_csv("quiz.csv", encoding='windows-1252', usecols=col_list)["explanation"]
        question_list = []
        for i in range(n):
            rand_ques_num = randint(0, len(list(questions))//2)
            question_list.append([list(questions)[rand_ques_num], list(answers)[rand_ques_num], list(explanation)[rand_ques_num]])
        # list_of_questions = zip(list(questions), list(answers), list(explanation))
        # return render(request, "index.html", {'ques': list_of_questions})
        return question_list
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def start(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            request.session['questions'] = get_questions(num_questions)
            request.session['qno'] = 0
            request.session['score'] = 0
            return render(request, 'instructions.html', {'user': username})
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def test_start(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            qno = int(request.session['qno'])
            q = list(request.session['questions'])
            s = int(request.session['score'])
            request.session['time'] = t = (datetime.now() + timedelta(minutes=quiz_time)).strftime("%Y-%m-%d %H:%M:%S")
            return render(request, 'quiz.html', {'user': username, 'ques': q[qno][0], 'num': qno+1, 'score': s, 'time_left': t})
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def next_ques(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            ans = request.POST['answer']
            qno = int(request.session['qno'])
            q = list(request.session['questions'])
            s = int(request.session['score'])
            t = request.session['time']
            if ans == q[qno][1]:
                request.session['score'] = s = s + 1
            global num_questions
            request.session['qno'] = qno = qno + 1
            if not qno == num_questions:
                return render(request, 'quiz.html', {'user': username, 'ques': q[qno][0], 'num': qno+1, 'score': s, 'time_left': t})
            else:
                return render(request, 'complete.html', {'user': username, 'score': s})
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def submit(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            try:
                name = request.user.get_full_name()
                usn = request.user.get_username()
                email = request.user.get_email_field_name()
                Register.objects.create(name=name, usn=usn, email=email, score1=int(request.session['score']))
                logout(request)
                return render(request, 'thanks.html')
            except Exception as e:
                return render(request, 'responded.html', {"user": request.user.get_full_name()})
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def skip_ques(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            qno = int(request.session['qno'])
            q = get_questions(1)
            s = int(request.session['score'])
            t = request.session['time']
            return render(request, 'quiz.html', {'user': username, 'ques': q[0][0], 'num': qno+1, 'score': s, 'time_left': t})
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def handler404(request, exception):
    context = {}
    response = render(request, '404.html', context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, '500.html', context)
    response.status_code = 500
    return response
