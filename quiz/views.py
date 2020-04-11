from django.template import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
from random import randint
from registration.models import Register, Instructions
from django.contrib.auth import logout
from datetime import datetime, timedelta
from quiz import settings

col_list = ["question_image", "correct_answer", "explanation"]

num_questions = int(Instructions.objects.get().num_questions)
quiz_time = int(Instructions.objects.get().test_time)
test_name = str(Instructions.objects.get().test_name)
test_num = int(Instructions.objects.get().test_number)


def get_questions(n, request):
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
            request.session['questions'] = get_questions(num_questions, request)
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
                """if test_num == 1:
                    Register.objects.filter(usn=request.user.get_username()).update(score1=s)
                elif test_num == 2:
                    Register.objects.filter(usn=request.user.get_username()).update(score2=s)
                elif test_num == 3:
                    Register.objects.filter(usn=request.user.get_username()).update(score3=s)
                elif test_num == 4:
                    Register.objects.filter(usn=request.user.get_username()).update(score4=s)
                elif test_num == 5:
                    Register.objects.filter(usn=request.user.get_username()).update(score5=s)"""
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
            usn = request.user.get_username()
            name = request.user.get_full_name()
            email = request.user.email

            if test_num == 1:
                try:
                    if str(Register.objects.get(pk=usn)) == str(usn):
                        if Register.objects.get(pk=usn).score1 == "":
                            Register.objects.filter(pk=usn).update(score1=int(request.session['score']))
                        else:
                            return render(request, 'responded.html', {"user": request.user.get_full_name()})
                except Exception as e:
                    Register.objects.create(name=name, usn=usn, email=email, score1=int(request.session['score']))
                logout(request)
                return render(request, 'thanks.html')
            elif test_num == 2:
                try:
                    if str(Register.objects.get(pk=usn)) == str(usn):
                        if Register.objects.get(pk=usn).score2 == "":
                            Register.objects.filter(pk=usn).update(score2=int(request.session['score']))
                        else:
                            return render(request, 'responded.html', {"user": request.user.get_full_name()})
                except Exception as e:
                    Register.objects.create(name=name, usn=usn, email=email, score2=int(request.session['score']))
                logout(request)
                return render(request, 'thanks.html')
            elif test_num == 3:
                try:
                    if str(Register.objects.get(pk=usn)) == str(usn):
                        if Register.objects.get(pk=usn).score3 == "":
                            Register.objects.filter(pk=usn).update(score3=int(request.session['score']))
                        else:
                            return render(request, 'responded.html', {"user": request.user.get_full_name()})
                except Exception as e:
                    Register.objects.create(name=name, usn=usn, email=email, score3=int(request.session['score']))
                logout(request)
                return render(request, 'thanks.html')
            elif test_num == 4:
                try:
                    if str(Register.objects.get(pk=usn)) == str(usn):
                        if Register.objects.get(pk=usn).score4 == "":
                            Register.objects.filter(pk=usn).update(score4=int(request.session['score']))
                        else:
                            return render(request, 'responded.html', {"user": request.user.get_full_name()})
                except Exception as e:
                    Register.objects.create(name=name, usn=usn, email=email, score4=int(request.session['score']))
                logout(request)
                return render(request, 'thanks.html')
            elif test_num == 5:
                try:
                    if str(Register.objects.get(pk=usn)) == str(usn):
                        if Register.objects.get(pk=usn).score5 == "":
                            Register.objects.filter(pk=usn).update(score5=int(request.session['score']))
                        else:
                            return render(request, 'responded.html', {"user": request.user.get_full_name()})
                except Exception as e:
                    Register.objects.create(name=name, usn=usn, email=email, score5=int(request.session['score']))
                logout(request)
                return render(request, 'thanks.html')

    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def skip_ques(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            q = list(request.session['questions'])
            qno = int(request.session['qno'])
            s = int(request.session['score'])
            t = request.session['time']
            qno = qno + 1
            if not qno == num_questions:
                request.session['qno'] = qno
                return render(request, 'quiz.html', {'user': username, 'ques': q[qno][0], 'num': qno+1, 'score': s, 'time_left': t})
            else:
                return render(request, 'complete.html', {'user': username, 'score': s})
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
