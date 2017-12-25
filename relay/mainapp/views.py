from django.shortcuts import render
from .forms import codeform
from django.http import HttpResponse, Http404, HttpResponseRedirect,JsonResponse
import requests, json
import time
from .models import *
# Create your views here.

def runcode(request):
    code = request.GET.get('code', None)
    input = request.GET.get('input', None)
    lang = request.GET.get('lang', None)
    langcode = {'4':1, '10':2, '26':3, '36':5, '35':30}
    lc = str(langcode[lang])
    t = str([str(input)])
    print(code)
    print([str(input)])
    print(langcode[lang])
    print(t)
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





def compiler(request):
    #start_time = time.time()
    #d = {'source':'print raw_input()', 'lang':'2', 'testcases':'["2"]','api_key':'hackerrank|2189697-2296|d21998aae507a388dd24d947e5c07073f8af7e44'}
    #d['source']='#include <iostream>\nint main() {\nstd::cout << "hello, world" << std::endl;\nreturn 0;\n}'
    #r = requests.post('http://api.hackerrank.com/checker/submission.json', data = d)
    #print(json.loads(r.text)["result"]["stdout"])
    #print("--- %s seconds ---" % (time.time() - start_time))
    if request.method== 'POST':
        print(request.POST)
        return render(request, "index.html", {'form': codeform()})

    else:
        return render(request, "index.html", {'form': codeform()})
