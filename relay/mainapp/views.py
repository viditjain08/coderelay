from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from ipware.ip import get_ip
import requests, json
import time
from.forms import registerform
from .models import *
import html
# Create your views here.


def ajaxregister(request):
    print("vidit")
    up = UserProfile.objects.filter(ip=get_ip)
    if up.exists()==False:
        print("reached0")
        form = registerform(request.POST)
        print(form)
        if request.method== 'POST':
            if form.is_valid():
                formdata=form.cleaned_data
                print(formdata)
                if formdata['password1']!=formdata['password2']:
                    error = "Passwords do no match"
                elif User.objects.filter(username=formdata['id']).count()>0:
                    error = "ID already registered"
                elif UserProfile.objects.filter(teamname=formdata['teamname']).count()>1:
                    error = "Teams cannot have more than 2 members"
                else:
                    u = UserProfile.objects.filter(teamname=formdata['teamname'])
                    if u.exists():
                        u1 = u[0].idno
                        user = authenticate(username=u1, password=formdata['password1'])
                        if user is not None:
                            u2 = User(username=formdata['id'], password=formdata['password1'])
                            u2.save()
                            u3 = UserProfile(user=u2, teamname=formdata['teamname'], idno=formdata['id'], ip=get_ip(request))
                            u3.save()
                        else:
                            error = "Password does not match with your teammate"
                    else:
                        u2 = User(username=formdata['id'], password=formdata['password1'])
                        u2.save()
                        u3 = UserProfile(user=u2, teamname=formdata['teamname'], idno=formdata['id'], ip=get_ip(request))
                        u3.save()
            else:
                pass
            data = {'error': error}
            print(data)
            return JsonResponse(data)
        else:
            return Http404("Something went wrong")
    else:
        return HttpResponse("This PC is already registered")


def register(request):
    return render(request, "register.html", {'form':registerform})


def runcode(request):
    code = request.GET.get('code', None)
    input = request.GET.get('input', None)
    lang = request.GET.get('lang', None)
    langcode = {'4':1, '10':2, '26':3, '36':5, '35':30}
    lc = str(langcode[lang])
    t = str([str(input)])
    start_time = time.time()
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
    return JsonResponse(data)


def savecode(request):
    code = request.GET.get('code', None)
    lang = request.GET.get('lang', None)
    langcode = {'4':1, '10':2, '26':3, '36':5, '35':30}
    lc = str(langcode[lang])
    c = Code.objects.get(pk=1)
    data = {
        'code': c.code,
        'lang': c.lang
    }
    return JsonResponse(data)


def compiler(request):
    #start_time = time.time()
    #d = {'source':'print raw_input()', 'lang':'2', 'testcases':'["2"]','api_key':'hackerrank|2189697-2296|d21998aae507a388dd24d947e5c07073f8af7e44'}
    #d['source']='#include <iostream>\nint main() {\nstd::cout << "hello, world" << std::endl;\nreturn 0;\n}'
    #r = requests.post('http://api.hackerrank.com/checker/submission.json', data = d)
    #print(json.loads(r.text)["result"]["stdout"])
    #print("--- %s seconds ---" % (time.time() - start_time))
    return render(request, "index.html")
