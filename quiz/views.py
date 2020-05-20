# import statements
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
import pandas as pd
from random import randint
from registration.models import Student, Instruction
from django.contrib.auth import logout
from datetime import datetime, timedelta
from quiz.settings import EMAIL_HOST_USER
import re
from collections import Counter

# List of columns in csv file
col_list = ["question_image", "correct_answer", "explanation"]

try:
    num_questions = int(Instruction.objects.get().num_questions) or 0
    quiz_time = int(Instruction.objects.get().test_time) or 0
    test_name = str(Instruction.objects.get().test_name) or "Default"
    test_num = int(Instruction.objects.get().test_number) or 1
except Exception as e:
    num_questions = 0
    quiz_time = 0
    test_name = "Enter Test name in Instructions"
    test_num = 1


def get_questions(n, request):
    try:
        questions = pd.read_csv("quiz"+str(test_num)+".csv", encoding='windows-1252', usecols=col_list)["question_image"]
        answers = pd.read_csv("quiz"+str(test_num)+".csv", encoding='windows-1252', usecols=col_list)["correct_answer"]
        explanation = pd.read_csv("quiz"+str(test_num)+".csv", encoding='windows-1252', usecols=col_list)["explanation"]
        questions = questions.dropna()
        answers = answers.dropna()
        ans = []
        for i in answers:
            if re.match("\d+\.\d+", str(i)):
                ans.append(int(i))
            else:
                ans.append(str(i))
        explanation = explanation.dropna()
        question_list = []
        rand_ques_num = []
        rand = randint(0, len(list(questions)) - 1)
        while len(rand_ques_num) < n:
            if rand not in rand_ques_num:
                rand_ques_num.append(rand)
            rand = randint(0, len(list(questions)) - 1)
        for i in range(n):
            question_list.append([list(questions)[rand_ques_num[i]], list(ans)[rand_ques_num[i]], list(explanation)[rand_ques_num[i]]])
        return question_list
    except Exception as e:
        print(e)
        request.status_code = 500
        return request


def start(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            request.session['questions'] = get_questions(num_questions, request)
            request.session['qno'] = 0
            request.session['score'] = 0
            return render(request, 'instructions.html', {'user': username, 'time': quiz_time, 'num_ques': num_questions})
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def test_start(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            qno = int(request.session['qno'])
            q = list(request.session['questions'])
            s = int(request.session['score'])
            email = request.user.email

            if test_num == 1:
                if not Student.objects.get(pk=email).score1 == "":
                    return render(request, 'responded.html', {"user": request.user.get_full_name()})
                else:
                    Student.objects.filter(pk=email).update(score1=0)
            elif test_num == 2:
                if not Student.objects.get(pk=email).score2 == "":
                    return render(request, 'responded.html', {"user": request.user.get_full_name()})
                else:
                    Student.objects.filter(pk=email).update(score2=0)
            elif test_num == 3:
                if not Student.objects.get(pk=email).score3 == "":
                    return render(request, 'responded.html', {"user": request.user.get_full_name()})
                else:
                    Student.objects.filter(pk=email).update(score3=0)
            elif test_num == 4:
                if not Student.objects.get(pk=email).score4 == "":
                    return render(request, 'responded.html', {"user": request.user.get_full_name()})
                else:
                    Student.objects.filter(pk=email).update(score4=0)
            elif test_num == 5 :
                if not Student.objects.get(pk=email).score5 == "":
                    return render(request, 'responded.html', {"user": request.user.get_full_name()})
                else:
                    Student.objects.filter(pk=email).update(score5=0)

            request.session['time'] = t = (datetime.now() + timedelta(minutes=quiz_time)).strftime("%Y-%m-%d %H:%M:%S")
            return render(request, 'quiz.html', {'user': username, 'ques': q[qno][0], 'num': qno+1, 'score': s, 'time_left': t})
    except Exception as e:
        return render(request, "error.html", {"user": request.user.get_full_name()})


def next_ques(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            username = request.user.get_full_name()
            ans = str(request.POST['answer'])
            qno = int(request.session['qno'])
            q = list(request.session['questions'])
            s = int(request.session['score'])
            t = request.session['time']
            if ans == str(q[qno][1]):
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
            email = request.user.email
            name = request.user.get_full_name()

            try:
                usn = Student.objects.get(pk=email).usn
            except:
                usn = email

            try:
                if str(request.POST["cheated"]) == "cheated":
                    try:
                        send_email(email, name, request.session['score'], True, request)
                    except:
                        pass
                    logout(request)
                    return render(request, 'cheating.html')
            except Exception as e:
                if test_num == 1:
                    try:
                        if str(Student.objects.get(pk=email)) == str(email):
                            if Student.objects.get(pk=email).score1 == "0" or 0:
                                Student.objects.filter(pk=email).update(score1=int(request.session['score']))
                                try:
                                    send_email(email, name, request.session['score'], False, request)
                                except:
                                    pass
                            else:
                                return render(request, 'responded.html', {"user": request.user.get_full_name()})
                    except Exception as e:
                        Student.objects.create(name=name, usn=usn, email=email, score1=int(request.session['score']))
                        try:
                            send_email(email, name, request.session['score'], False, request)
                        except:
                            pass
                    logout(request)
                    return render(request, 'thanks.html')
                elif test_num == 2:
                    try:
                        if str(Student.objects.get(pk=email)) == str(email):
                            if Student.objects.get(pk=email).score2 == "0" or 0:
                                Student.objects.filter(pk=email).update(score2=int(request.session['score']))
                                try:
                                    send_email(email, name, request.session['score'], False, request)
                                except:
                                    pass
                            else:
                                return render(request, 'responded.html', {"user": request.user.get_full_name()})
                    except Exception as e:
                        Student.objects.create(name=name, usn=usn, email=email, score2=int(request.session['score']))
                        try:
                            send_email(email, name, request.session['score'], False, request)
                        except:
                            pass
                    logout(request)
                    return render(request, 'thanks.html')
                elif test_num == 3:
                    try:
                        if str(Student.objects.get(pk=email)) == str(email):
                            if Student.objects.get(pk=email).score3 == "0" or 0:
                                Student.objects.filter(pk=email).update(score3=int(request.session['score']))
                                try:
                                    send_email(email, name, request.session['score'], False, request)
                                except:
                                    pass
                            else:
                                return render(request, 'responded.html', {"user": request.user.get_full_name()})
                    except Exception as e:
                        Student.objects.create(name=name, usn=usn, email=email, score3=int(request.session['score']))
                        try:
                            send_email(email, name, request.session['score'], False, request)
                        except:
                            pass
                    logout(request)
                    return render(request, 'thanks.html')
                elif test_num == 4:
                    try:
                        if str(Student.objects.get(pk=email)) == str(email):
                            if Student.objects.get(pk=email).score4 == "0" or 0:
                                Student.objects.filter(pk=email).update(score4=int(request.session['score']))
                                try:
                                    send_email(email, name, request.session['score'], False, request)
                                except:
                                    pass
                            else:
                                return render(request, 'responded.html', {"user": request.user.get_full_name()})
                    except Exception as e:
                        Student.objects.create(name=name, usn=usn, email=email, score4=int(request.session['score']))
                        try:
                            send_email(email, name, request.session['score'], False, request)
                        except:
                            pass
                    logout(request)
                    return render(request, 'thanks.html')
                elif test_num == 5:
                    try:
                        if str(Student.objects.get(pk=email)) == str(email):
                            if Student.objects.get(pk=email).score5 == "0" or 0:
                                Student.objects.filter(pk=email).update(score5=int(request.session['score']))
                                try:
                                    send_email(email, name, request.session['score'], False, request)
                                except:
                                    pass
                            else:
                                return render(request, 'responded.html', {"user": request.user.get_full_name()})
                    except Exception as e:
                        Student.objects.create(name=name, usn=usn, email=email, score5=int(request.session['score']))
                        try:
                            send_email(email, name, request.session['score'], False, request)
                        except:
                            pass
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


def home(request):
    return render(request, "index.html")


def send_email(email, name, score, ch, questions):
    try:
        if not ch:
            subject = 'Thank You for taking '+str(test_name)
            html_message = render_to_string('email.html', {'user': name, 'score': score, 'test_name': test_name,
                                                           'cheat': False, 'admin': False, 'num': num_questions})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, "Efkairies CMRIT <"+EMAIL_HOST_USER+">", [str(email)], html_message=html_message)

            subject = 'Result for User ' + str(name)
            html_message = render_to_string('email.html',
                                            {'user': name, 'score': score, 'test_name': test_name, 'cheat': False,
                                             'admin': True, 'ques': list(questions.session['questions']), 'num': num_questions})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, "Efkairies CMRIT <" + EMAIL_HOST_USER + ">", [str(EMAIL_HOST_USER)], html_message=html_message)
        else:
            subject = 'Tab Switch Triggered for '+str(name)
            html_message = render_to_string('email.html', {'user': name, 'score': score, 'test_name': test_name,
                                                           'cheat': True, 'admin': False, 'num': num_questions})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, "Efkairies CMRIT <" + EMAIL_HOST_USER + ">",  [str(email), str(EMAIL_HOST_USER)],
                      html_message=html_message)
    except Exception as e:
        subject = 'Error sending email confirmation'
        message = 'The User <strong>' + str(name) + \
                  "</strong>,<br><br>Has successfully completed " + str(test_name) + \
                  "<br>His/Her score is: " + str(score) + \
                  "<br><br>Mail Timestamp: <code>" + str(datetime.now().strftime("%H:%M:%S %d-%m-%Y ")) + \
                  "</code><br><br>Thank You" \
                  "<br>Team Efkairies"
        msg = EmailMessage(subject, message, "Efkairies CMRIT <" + EMAIL_HOST_USER + ">", [str(email), str(EMAIL_HOST_USER)])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        # send_mail(subject, message, EMAIL_HOST_USER, [str(EMAIL_HOST_USER)], fail_silently=False)


def result(pwd):
    try:
        if re.findall('pwd=0x\w+', str(pwd))[0] == "pwd=0xbeepboop":
            obj = Student.objects.all()
            all = []
            chart = []
            for a in obj:
                all.append([a.name, a.usn, a.score1, a.score2, a.score3, a.score4, a.score5])
            if test_num == 1:
                count = Student.objects.filter(score1__regex='\d+').count()
                for i in range(len(all)):
                    if not all[i][2] == '':
                        chart.append(int(all[i][2]))
                # ab = Student.objects.aggregate(Sum('score1'))
            elif test_num == 2:
                count = Student.objects.filter(score2__regex='\d+').count()
                for i in range(len(all)):
                    if not all[i][3] == '':
                        chart.append(int(all[i][3]))
            elif test_num == 3:
                count = Student.objects.filter(score3__regex='\d+').count()
                for i in range(len(all)):
                    if not all[i][4] == '':
                        chart.append(int(all[i][4]))
            elif test_num == 4:
                count = Student.objects.filter(score4__regex='\d+').count()
                for i in range(len(all)):
                    if not all[i][5] == '':
                        chart.append(int(all[i][5]))
            elif test_num == 5:
                count = Student.objects.filter(score5__regex='\d+').count()
                for i in range(len(all)):
                    if not all[i][6] == '':
                        chart.append(int(all[i][6]))

            dm = Counter(chart)
            dictOfMarks = {}
            for i in sorted(dm):
                dictOfMarks[i] = dm[i]

            # results = zip(obj.values('name'), obj.values('usn'), obj.values('score1'), obj.values('score2'), obj.values('score3'), obj.values('score4'), obj.values('score5'))
            return render(pwd, "result.html", {'results': all,
                                               'test_name': test_name,
                                               'num_reg': Student.objects.count(),
                                               'sub': count,
                                               'val': (count/Student.objects.count())*100,
                                               'values': str(dictOfMarks.values())[12:-1],
                                               'axis': str(dictOfMarks.keys())[10:-1]})
        else:
            return render(pwd, '404.html')
    except Exception as e:
        return render(pwd, "404.html")
