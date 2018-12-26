# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import ItunesScript
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .dataparse import DataParse
import os
import json


def index(request):
    # script_list = get_object_or_404(ItunesScript, name__startswith='itunes')
    try:
        script_list = ItunesScript.objects.filter(name__startswith='itunes')
        script_list_dp = script_list.filter(name__contains='get')
        # print(script_list_dp)
    except ItunesScript.Doesnotexist:
        raise Http404("Script doesn\'t exist.")
    context = {
        'script_list': script_list,
        'script_list_dp': script_list_dp
    }

    return HttpResponse(render(request, 'itunes/index.html', context))


def get_content(request, script_id):
    script_name = ItunesScript.objects.get(id=script_id).name
    script_path = ItunesScript.objects.get(id=script_id).path
    filename = script_path + script_name

    script_content = ItunesScript().read_script(filename)
    return HttpResponse(script_content)


def list(request):
    script_list = ItunesScript.objects.filter(name__startswith='itunes')
    output = ','.join([q.name for q in script_list])
    return HttpResponse(output)


def execute_script(request, script_id):
    script_name = ItunesScript.objects.get(id=script_id).name
    script_path = ItunesScript.objects.get(id=script_id).path
    filename = script_path + script_name

    print(filename)
    con = filename

#   使用os模块的popen方法来读取命令执行返回值。
    try:
        # command = 'osascript -s s ' + con
        # output = os.popen(command).readlines()
        os.system('osascript ' + con)
        output = "success"
    except 'Exception':
        output = "fail"

    context = {
        'output': output
    }
    return HttpResponse(render(request, 'itunes/execute.html', context))


def execute_script_dp(request, script_id):
    script_name = ItunesScript.objects.get(id=script_id).name
    script_path = ItunesScript.objects.get(id=script_id).path
    filename = script_path + script_name

    print(filename)
    con = filename

    try:
        command = 'osascript -s s ' + con
        output = os.popen(command).readlines()
    except 'Exception':
        output = "fail"

    # print('before dp ' + str(output))
    dp = DataParse
    output = DataParse.dp_itunes(dp, output[0])
    output = json.dumps(output, ensure_ascii=False)
    # print('after dp ' + str(output))

    return HttpResponse(output)


def list_script(request, script_id):
    script_path = ItunesScript.objects.get(id=script_id).path
    script_list = []
    for filename in os.listdir(script_path):
        script_list.append(filename)
    return HttpResponse(script_list)


def insert_script(request):
    filepath = 'scripts/'
    output = []
    num = 0
    SCRIPT_NAME='itunes'
    for filename in os.listdir(filepath):
        if filename.split('_')[0] == SCRIPT_NAME:
            queue = ItunesScript.objects.all()
#            print(queue)
#            print(queue.count())
            if queue.count() == 0:
                num = num + 1
                ItunesScript.objects.create(name=filename, path=filepath)
                output.append('Record ' + str(num) + ' insert success.')
                # output.append('\r\n')
            else:
                flag = 0
                for sid in range(queue.count() + 1):
                    try:
                        if queue.get(id=sid).name == filename:
                            flag = flag + 1
                        else:
                            flag = flag
                    except:
                        pass
                if flag == 0:
                    num = num + 1
                    ItunesScript.objects.create(name=filename, path=filepath)
                    output.append('Record ' + str(num) + ' insert success.')
                    # output.append('\r\n')
                else:
                    num = num + 1
                    output.append('Script ' + filename + ' already exsists.')
                    # output.append('\r\n')
        else:
            output.append('This script does not start as ' + SCRIPT_NAME + '.')
            # output.append('\r\n')
    context = {
        'output': output
    }
    return HttpResponse(render(request, 'itunes/insert.html', context))

