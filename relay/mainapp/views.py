from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from ipware.ip import get_ip
from django.contrib.auth.decorators import login_required
from random import randint
import requests, json
import time
from.forms import registerform, loginform
from .models import *
import html
# Create your views here.


def ajaxregister(request):
    print("vidit")
    error = ''
    success = False
    register_errors = []
    up = UserProfile.objects.filter(ip=get_ip(request))
    if up.exists()==False:
        print("reached0")
        form = registerform(request.POST)
        reg_errors=json.loads(json.dumps(form.errors))
        for k,v in reg_errors.items():
            if v==['This field is required.']:
                register_errors.append("All fields are required")
            else:
                register_errors.append(v)
            error = register_errors[0]
        if request.method== 'POST':
            if form.is_valid():
                print("1")
                formdata=form.cleaned_data
                if User.objects.filter(username=formdata['id']).count()>0:
                    error = "ID already registered"
                elif UserProfile.objects.filter(teamname=formdata['teamname']).count()>1:
                    error = "Teams cannot have more than 2 members"
                else:
                    u = UserProfile.objects.filter(teamname=formdata['teamname'])
                    if u.exists():
                        u1 = u[0].idno
                        user = authenticate(username=u1, password=formdata['password1'])
                        if user is not None:
                            u2 = User(username=formdata['id'])
                            u2.set_password(formdata['password1'])
                            u2.save()
                            u3 = UserProfile(user=u2, teamname=formdata['teamname'], name=formdata['name'], idno=formdata['id'], ip=get_ip(request))
                            u3.save()
                            try:
                                t = Team.objects.get(user1=u)
                                t.user2 = u3
                                t.save()
                                success = True
                            except:
                                error = "Something went wrong"
                        else:
                            error = "Password does not match with your teammate"
                    else:
                        u2 = User(username=formdata['id'])
                        u2.set_password(formdata['password1'])
                        u2.save()
                        u3 = UserProfile(user=u2, teamname=formdata['teamname'], name=formdata['name'], idno=formdata['id'], ip=get_ip(request))
                        u3.save()
                        t = Team(user1=u3)
                        t.save()
                        success = True

            else:
                pass
            data = {'error': error, 'success': success}
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': "Something went wrong", 'success': success})
    else:
        return JsonResponse({'error': "This PC is already registered", 'success': success})


def register(request):
    return render(request, "register.html", {'form':registerform})

def login(request):
    if request.user.is_authenticated:
        #If user logged in, redirect to home page
        return HttpResponseRedirect('/')
    return render(request, "login.html", {'form':loginform})

def loginregister(request):
    if request.user.is_authenticated:
        #If user logged in, redirect to game
        return HttpResponseRedirect('/game')
    return render(request, "loginregister.html", {'loginform':loginform, 'registerform':registerform})


def ajaxlogin(request):
    print("vidit")
    print(request.POST)
    success = False
    error = ''
    up = UserProfile.objects.filter(ip=get_ip(request))
    print(get_ip(request))
    try:
        t = Team.objects.get(Q(user1=up)|Q(user2=up))
        if t.user2 is None:
            error = "Your teammate hasn't registered"
            return JsonResponse({'error': error, 'success': success})
    except:
        error = "Something happened"
    if up.exists()==True:
        print("reached0")
        form = loginform(request.POST)
        print(form)
        if request.method== 'POST':
            if form.is_valid():
                formdata=form.cleaned_data
                print(formdata)
                username = formdata['id']
                password = formdata['password']
                u = User.objects.filter(username=formdata['id'])
                if u.count()>0 and u[0]!=up[0].user:
                    error = "ID registered from other pc"
                elif u.count()==0:
                    error = "ID not registered"
                else:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        authlogin(request, user)
                        try:
                            u1 = UserProfile.objects.get(user=user)
                            t = Team.objects.filter(Q(user1=u1) | Q(user2=u1))[0]
                            if t.time<time.time():
                                t.time = time.time()+randint(130,140)
                                t.save()
                            success = True
                        except:
                            error = "Something went wrong"
                            

                    else:
                        error = "Invalid Password"

            else:
                error = "Invalid ID"
            data = {'error': error, 'success': success}
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': "Something went wrong"})
    else:
        return JsonResponse({'error': "This PC is not registered"})


def logout(request):
    authlogout(request)
    return HttpResponseRedirect('/login')


def runcode(request):
    code = request.GET.get('code', None)
    input = request.GET.get('input', None)
    lang = request.GET.get('lang', None)
    langcode = {'4':1, '10':2, '26':3, '36':5, '35':30}
    u = UserProfile.objects.get(user=request.user)
    t = Team.objects.get(Q(user1=u) | Q(user2=u))
    if t.enable==False:
        return JsonResponse({'finish': True})
    lc = str(langcode[lang])
    t = str([str(input)])
    start_time = time.time()
    try:
        d = {'source': code, 'lang': lc, 'testcases': t,
             'api_key': 'hackerrank|2189697-2296|d21998aae507a388dd24d947e5c07073f8af7e44'}
        r = requests.post('http://api.hackerrank.com/checker/submission.json', data=d)
        print(json.loads(r.text))
        abc = json.loads(r.text)
        print("--- %s seconds ---" % (time.time() - start_time))
        data = {
            'compiles': abc["result"]["stderr"]==[False],
        }
        if data['compiles']:
            data['output'] = abc["result"]["stdout"]
        else:
            data['output'] = abc["result"]["stderr"]
        print(data)
    except:
        data = {'output': "Some error occured", 'compiles': False}
    return JsonResponse(data)


def swapcode(request):
    u = UserProfile.objects.get(user=request.user)
    t = Team.objects.get(Q(user1=u) | Q(user2=u))
    if t.enable==False:
        return JsonResponse({'finish': True})
    if t.user1q is None or t.user2q is None:
        return JsonResponse({'finish': True})
    if t.user1==u:
        c1 = Code.objects.get(team=t,question=t.user1q)
        c1.swap=True
        c1.save()
        c2 = Code.objects.get(team=t,question=t.user2q)
        while c2.swap==False:
            c2 = Code.objects.get(team=t,question=t.user2q)
        t.user2q = t.user1q
        c2.swap = False
        c2.save()
        t.save()
    else:
        c1 = Code.objects.get(team=t,question=t.user2q)
        c1.swap=True
        c1.save()
        c2 = Code.objects.get(team=t,question=t.user1q)
        while c2.swap==False:
            c2 = Code.objects.get(team=t,question=t.user1q)
        t.user1q = t.user2q
        c2.swap = False
        c2.save()
        t.time = time.time()+randint(300,400)
        t.save()
    return JsonResponse({'question': c2.question.question_text, 'heading': c2.question.heading, 'code': c2.code, 'lang': c2.lang, 'time': t.time})

def savecode(request):
    code = request.GET.get('code', None)
    lang = request.GET.get('lang', None)
    u = UserProfile.objects.get(user=request.user)
    t = Team.objects.get(Q(user1=u) | Q(user2=u))
    if t.enable==False:
        return JsonResponse({'finish': True})

    if t.user1==u:
        q = t.user1q
    else:
        q = t.user2q
    try:
        cd = Code.objects.get(team=t,question=q)
        cd.code=code
        cd.lang=int(lang)
        cd.save()
    except:
        cd = Code(team=t, question=q, code=code, lang=int(lang))
        cd.save()
    return JsonResponse({})


def finishrace(request):
    code = request.GET.get('code', None)
    lang = request.GET.get('lang', None)
    u = UserProfile.objects.get(user=request.user)
    t = Team.objects.get(Q(user1=u) | Q(user2=u))
    ques_list = Question.objects.all()
    t.enable=False
    t.save()
    if t.user1==u:
        q = t.user1q
    else:
        q = t.user2q
    try:
        cd = Code.objects.get(team=t,question=q)
        cd.code=code
        cd.lang=int(lang)
        cd.save()
    except:
        cd = Code(team=t, question=q, code=code, lang=int(lang))
        cd.save()
    return JsonResponse({'finish':True})

def submitques(request):
    code = request.GET.get('code', None)
    lang = request.GET.get('lang', None)
    ques_list = Question.objects.all()
    u = UserProfile.objects.get(user=request.user)
    t = Team.objects.get(Q(user1=u) | Q(user2=u))
    if t.enable==False:
        print("vidit")
        return JsonResponse({'finish': True})
    print(t)
    if t.user1==u:
        q = t.user1q
        print("1")
    else:
        q = t.user2q
        print("2")

    try:
        cd = Code.objects.get(team=t,question=q)
        cd.code=code
        cd.lang=int(lang)
        cd.save()
        print("3")
    except:
        cd = Code(team=t, question=q, code=code, lang=int(lang))
        cd.save()
    qlist = [x for x in ques_list]
    try:

        if t.user1==u:
            x = t.user1q = ques_list[max(qlist.index(t.user1q),qlist.index(t.user2q))+1]
        else:
            x = t.user2q = ques_list[max(qlist.index(t.user1q),qlist.index(t.user2q))+1]
        t.save()
    except:
        return JsonResponse({'question': cd.question.question_text, 'heading': cd.heading, 'done': True})               
    return JsonResponse({'question': x.question_text, 'heading': x.heading})



def abcd(request):
    return render(request, "index1.html")


@login_required(login_url='/')
def compiler(request):
    #start_time = time.time()
    #d = {'source':'print raw_input()', 'lang':'2', 'testcases':'["2"]','api_key':'hackerrank|2189697-2296|d21998aae507a388dd24d947e5c07073f8af7e44'}
    #d['source']='#include <iostream>\nint main() {\nstd::cout << "hello, world" << std::endl;\nreturn 0;\n}'
    #r = requests.post('http://api.hackerrank.com/checker/submission.json', data = d)
    #print(json.loads(r.text)["result"]["stdout"])
    #print("--- %s seconds ---" % (time.time() - start_time))
    try:
        g = GameSwitch.objects.get(pk=1)
        if g.game_active==0:
            return HttpResponse("Something went wrong")
    except:
        return HttpResponse("Something went wrong")
    u = UserProfile.objects.get(user=request.user)
    t = Team.objects.get(Q(user1=u) | Q(user2=u))
    if t.enable==False:
        authlogout(request)
        return HttpResponseRedirect('/') 

    ques_list = Question.objects.all()
    if t.user1==u:
        q = t.user1q
        if q is None:
            code = Code(question=ques_list[0], team=t)
            t.user1q=ques_list[0]
            t.save()
        else:
            try:
                code = Code.objects.get(question=q,team=t)
            except:
                code = Code(question=q, team=t)
    else:
        q = t.user2q
        if q is None:
            code = Code(question=ques_list[1], team=t)
            t.user2q=ques_list[1]
            t.save()
        else:
            try:
                code = Code.objects.get(question=q,team=t)
            except:
                code = Code(question=q, team=t)
    print(code.code)
    return render(request, "game.html",{'user': u, 'team': t, 'time':t.time, 'code': code})
